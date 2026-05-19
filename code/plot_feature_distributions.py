#!/usr/bin/env python3
"""
Генератор диагностических распределений для выбранных признаков.

Зачем:
- быстро посмотреть, не выглядят ли признаки испорченными: клиппинг, дискретизация,
  странные пики, сильный сдвиг train/test, разные распределения по target;
- сохранить картинки и таблицу со статистиками для дальнейшего анализа.

Примеры запуска:

1) Несколько конкретных признаков:
   python plot_feature_distributions.py \
       --csv ./ml-project-adaai_VK_predict_hackaton/data/train.csv \
       --features feature_1,feature_7,feature_42

2) Диапазон признаков feature_0 ... feature_30:
   python plot_feature_distributions.py --features 0-30

3) Все feature_*:
   python plot_feature_distributions.py --features all

4) Сравнить train и test по тем же признакам:
   python plot_feature_distributions.py \
       --csv ./ml-project-adaai_VK_predict_hackaton/data/train.csv \
       --compare-csv ./ml-project-adaai_VK_predict_hackaton/data/test.csv \
       --features 0-50

Результат:
- PNG по каждому признаку в папке --out-dir;
- feature_distribution_summary.csv со статистиками;
- suspicious_features.csv с простыми эвристическими флагами.
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy import stats as scipy_stats
except Exception:  # scipy может быть не установлен, скрипт всё равно будет работать
    scipy_stats = None


DEFAULT_CSV = "./ml-project-adaai_VK_predict_hackaton/data/train.csv"
DEFAULT_COMPARE_CSV = None
DEFAULT_OUT_DIR = "./ml-project-adaai_VK_predict_hackaton/distribution_plots"
DEFAULT_TARGET_COL = "target"
DEFAULT_INDEX_COLS = ("index",)


# ----------------------------- parsing features -----------------------------

def _natural_feature_key(col: str) -> tuple[int, str]:
    """Сортировка feature_2 раньше feature_10."""
    m = re.search(r"(\d+)$", str(col))
    return (int(m.group(1)) if m else 10**12, str(col))


def parse_feature_spec(spec: str, columns: Iterable[str], exclude: set[str]) -> list[str]:
    """
    Поддерживаемые форматы:
    - all
    - feature_1,feature_2,feature_10
    - 1,2,10                -> feature_1, feature_2, feature_10, если такие есть
    - 0-50                  -> feature_0 ... feature_50
    - feature_0-feature_50  -> feature_0 ... feature_50
    """
    columns = list(columns)
    col_set = set(columns)
    candidate_features = [c for c in columns if c not in exclude]

    if spec.strip().lower() == "all":
        return sorted(candidate_features, key=_natural_feature_key)

    selected: list[str] = []
    chunks = [x.strip() for x in spec.split(",") if x.strip()]

    for chunk in chunks:
        # Диапазоны: 1-10 или feature_1-feature_10
        range_match = re.fullmatch(r"(?:feature_)?(\d+)\s*-\s*(?:feature_)?(\d+)", chunk)
        if range_match:
            start, end = map(int, range_match.groups())
            step = 1 if start <= end else -1
            for num in range(start, end + step, step):
                name = f"feature_{num}"
                if name in col_set:
                    selected.append(name)
            continue

        # Номер признака: 42 -> feature_42
        if re.fullmatch(r"\d+", chunk):
            name = f"feature_{int(chunk)}"
            if name in col_set:
                selected.append(name)
            else:
                print(f"[WARN] Нет колонки {name}, пропускаю")
            continue

        # Явное имя колонки
        if chunk in col_set:
            selected.append(chunk)
        else:
            print(f"[WARN] Нет колонки {chunk}, пропускаю")

    # Убираем дубли, сохраняя порядок
    unique_selected = []
    seen = set()
    for col in selected:
        if col not in seen and col not in exclude:
            unique_selected.append(col)
            seen.add(col)

    return unique_selected


# ----------------------------- stats / heuristics ----------------------------

def numeric_summary(s: pd.Series) -> dict[str, float | int | str | None]:
    x = pd.to_numeric(s, errors="coerce").dropna()
    n_total = len(s)
    n = len(x)

    out: dict[str, float | int | str | None] = {
        "n_total": n_total,
        "n_non_na": n,
        "n_missing": n_total - n,
        "missing_ratio": (n_total - n) / n_total if n_total else np.nan,
        "n_unique": int(x.nunique()) if n else 0,
        "top_freq_ratio": np.nan,
        "min": np.nan,
        "q01": np.nan,
        "q05": np.nan,
        "q25": np.nan,
        "median": np.nan,
        "mean": np.nan,
        "q75": np.nan,
        "q95": np.nan,
        "q99": np.nan,
        "max": np.nan,
        "std": np.nan,
        "skew": np.nan,
        "kurtosis": np.nan,
        "zero_ratio": np.nan,
        "negative_ratio": np.nan,
    }

    if n == 0:
        return out

    vc = x.value_counts(dropna=False, normalize=True)
    qs = x.quantile([0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99])

    out.update({
        "top_freq_ratio": float(vc.iloc[0]),
        "min": float(x.min()),
        "q01": float(qs.loc[0.01]),
        "q05": float(qs.loc[0.05]),
        "q25": float(qs.loc[0.25]),
        "median": float(qs.loc[0.50]),
        "mean": float(x.mean()),
        "q75": float(qs.loc[0.75]),
        "q95": float(qs.loc[0.95]),
        "q99": float(qs.loc[0.99]),
        "max": float(x.max()),
        "std": float(x.std(ddof=1)) if n > 1 else 0.0,
        "skew": float(x.skew()) if n > 2 else np.nan,
        "kurtosis": float(x.kurtosis()) if n > 3 else np.nan,
        "zero_ratio": float((x == 0).mean()),
        "negative_ratio": float((x < 0).mean()),
    })
    return out


def make_flags(row: pd.Series) -> str:
    """Грубые признаки, которые стоит глазами проверить на графиках."""
    flags = []

    n = row.get("n_non_na", np.nan)
    n_unique = row.get("n_unique", np.nan)
    top_freq = row.get("top_freq_ratio", np.nan)
    std = row.get("std", np.nan)
    q01, q99 = row.get("q01", np.nan), row.get("q99", np.nan)
    mn, mx = row.get("min", np.nan), row.get("max", np.nan)
    skew = row.get("skew", np.nan)
    kurt = row.get("kurtosis", np.nan)

    if pd.notna(n_unique) and n_unique <= 2:
        flags.append("almost_binary")
    elif pd.notna(n_unique) and pd.notna(n) and n_unique <= max(10, 0.001 * n):
        flags.append("very_discrete")

    if pd.notna(top_freq) and top_freq >= 0.50:
        flags.append("one_value_dominates")

    if pd.notna(std) and std == 0:
        flags.append("constant")

    # Если минимум/максимум ровно совпадают с 1%/99% квантилем, часто это похоже на клиппинг/обрезку.
    if pd.notna(mn) and pd.notna(q01) and math.isclose(mn, q01, rel_tol=0, abs_tol=1e-12):
        flags.append("left_edge_mass")
    if pd.notna(mx) and pd.notna(q99) and math.isclose(mx, q99, rel_tol=0, abs_tol=1e-12):
        flags.append("right_edge_mass")

    if pd.notna(skew) and abs(skew) >= 3:
        flags.append("high_skew")
    if pd.notna(kurt) and kurt >= 20:
        flags.append("heavy_tails")

    return ";".join(flags)


def train_test_drift(train_s: pd.Series, test_s: pd.Series) -> dict[str, float | None]:
    """Простые меры сдвига между train/test для числового признака."""
    x = pd.to_numeric(train_s, errors="coerce").dropna().to_numpy()
    y = pd.to_numeric(test_s, errors="coerce").dropna().to_numpy()

    if len(x) == 0 or len(y) == 0:
        return {"ks_stat_train_test": np.nan, "ks_pvalue_train_test": np.nan, "mean_shift_std_units": np.nan}

    pooled_std = np.nanstd(np.concatenate([x, y]), ddof=1)
    mean_shift = abs(np.nanmean(x) - np.nanmean(y)) / pooled_std if pooled_std > 0 else 0.0

    if scipy_stats is not None:
        ks = scipy_stats.ks_2samp(x, y)
        return {
            "ks_stat_train_test": float(ks.statistic),
            "ks_pvalue_train_test": float(ks.pvalue),
            "mean_shift_std_units": float(mean_shift),
        }

    return {
        "ks_stat_train_test": np.nan,
        "ks_pvalue_train_test": np.nan,
        "mean_shift_std_units": float(mean_shift),
    }


# -------------------------------- plotting -----------------------------------

def _finite_numeric(s: pd.Series) -> np.ndarray:
    arr = pd.to_numeric(s, errors="coerce").to_numpy(dtype=float)
    return arr[np.isfinite(arr)]


def _safe_bins(x: np.ndarray, max_bins: int = 80) -> int:
    if len(x) <= 1:
        return 1
    unique = len(np.unique(x))
    if unique <= 30:
        return unique
    # Freedman-Diaconis rule with sane bounds
    q25, q75 = np.percentile(x, [25, 75])
    iqr = q75 - q25
    if iqr <= 0:
        return min(max_bins, max(10, int(np.sqrt(len(x)))))
    bin_width = 2 * iqr / (len(x) ** (1 / 3))
    if bin_width <= 0:
        return min(max_bins, max(10, int(np.sqrt(len(x)))))
    bins = int(np.ceil((np.nanmax(x) - np.nanmin(x)) / bin_width))
    return int(np.clip(bins, 5, max_bins))


def _plot_kde_if_possible(ax, x: np.ndarray, label: str | None = None) -> None:
    if scipy_stats is None or len(x) < 5 or np.nanstd(x) == 0:
        return
    try:
        kde = scipy_stats.gaussian_kde(x)
        grid = np.linspace(np.nanmin(x), np.nanmax(x), 300)
        ax.plot(grid, kde(grid), linewidth=2, label=label)
    except Exception:
        return


def _plot_ecdf(ax, x: np.ndarray, label: str) -> None:
    if len(x) == 0:
        return
    xs = np.sort(x)
    ys = np.arange(1, len(xs) + 1) / len(xs)
    ax.plot(xs, ys, label=label)


def plot_feature(
    train_df: pd.DataFrame,
    feature: str,
    out_dir: Path,
    target_col: str | None = DEFAULT_TARGET_COL,
    compare_df: pd.DataFrame | None = None,
    top_n_values: int = 20,
) -> None:
    s = train_df[feature]
    x = _finite_numeric(s)
    has_target = target_col is not None and target_col in train_df.columns
    has_compare = compare_df is not None and feature in compare_df.columns

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(f"Distribution diagnostics: {feature}", fontsize=16)

    # 1) Histogram + optional KDE / train-test overlay
    ax = axes[0, 0]
    if len(x) > 0:
        bins = _safe_bins(x)
        ax.hist(x, bins=bins, density=True, alpha=0.35, label="train")
        _plot_kde_if_possible(ax, x, label="train KDE")

        if has_compare:
            y = _finite_numeric(compare_df[feature])
            if len(y) > 0:
                ax.hist(y, bins=bins, density=True, alpha=0.25, label="compare/test")
                _plot_kde_if_possible(ax, y, label="compare/test KDE")

        ax.set_title("Histogram / density")
        ax.set_xlabel(feature)
        ax.set_ylabel("density")
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No numeric values", ha="center", va="center")
        ax.set_axis_off()

    # 2) By target or boxplot
    ax = axes[0, 1]
    if len(x) > 0 and has_target:
        plotted = False
        bins = _safe_bins(x)
        for cls in sorted(train_df[target_col].dropna().unique()):
            cls_x = _finite_numeric(train_df.loc[train_df[target_col] == cls, feature])
            if len(cls_x) > 0:
                ax.hist(cls_x, bins=bins, density=True, alpha=0.35, label=f"target={cls}")
                plotted = True
        if plotted:
            ax.set_title("Distribution by target")
            ax.set_xlabel(feature)
            ax.set_ylabel("density")
            ax.legend()
        else:
            ax.text(0.5, 0.5, "No target groups", ha="center", va="center")
            ax.set_axis_off()
    elif len(x) > 0:
        ax.boxplot(x, vert=False, showfliers=True)
        ax.set_title("Boxplot")
        ax.set_xlabel(feature)
    else:
        ax.text(0.5, 0.5, "No numeric values", ha="center", va="center")
        ax.set_axis_off()

    # 3) ECDF: хорошо видно клиппинг/ступеньки/сдвиг train-test
    ax = axes[1, 0]
    if len(x) > 0:
        _plot_ecdf(ax, x, "train")
        if has_compare:
            y = _finite_numeric(compare_df[feature])
            _plot_ecdf(ax, y, "compare/test")
        ax.set_title("ECDF")
        ax.set_xlabel(feature)
        ax.set_ylabel("cumulative probability")
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No numeric values", ha="center", va="center")
        ax.set_axis_off()

    # 4) Top values / spikes
    ax = axes[1, 1]
    vc = s.value_counts(dropna=False).head(top_n_values)
    if len(vc) > 0:
        labels = [str(v)[:28] for v in vc.index]
        ax.bar(range(len(vc)), vc.values)
        ax.set_xticks(range(len(vc)))
        ax.set_xticklabels(labels, rotation=60, ha="right")
        ax.set_title(f"Top {min(top_n_values, len(vc))} values / spikes")
        ax.set_ylabel("count")
    else:
        ax.text(0.5, 0.5, "No values", ha="center", va="center")
        ax.set_axis_off()

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out_path = out_dir / f"{feature}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_all_features(
    train_df: pd.DataFrame,
    features: list[str],
    out_dir: Path,
    target_col: str | None,
    compare_df: pd.DataFrame | None,
    top_n_values: int,
) -> pd.DataFrame:
    rows = []

    for i, feature in enumerate(features, start=1):
        print(f"[{i}/{len(features)}] {feature}")

        row = {"feature": feature}
        row.update(numeric_summary(train_df[feature]))

        if compare_df is not None and feature in compare_df.columns:
            row.update(train_test_drift(train_df[feature], compare_df[feature]))

        rows.append(row)
        plot_feature(
            train_df=train_df,
            feature=feature,
            out_dir=out_dir,
            target_col=target_col,
            compare_df=compare_df,
            top_n_values=top_n_values,
        )

    summary = pd.DataFrame(rows)
    if not summary.empty:
        summary["flags"] = summary.apply(make_flags, axis=1)
    return summary


# ----------------------------------- main ------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Строит диагностические графики распределений для выбранных признаков."
    )
    parser.add_argument("--csv", default=DEFAULT_CSV, help="Путь к train CSV")
    parser.add_argument("--compare-csv", default=DEFAULT_COMPARE_CSV, help="Опционально: CSV для сравнения, например test.csv")
    parser.add_argument("--features", default="all", help="all, список колонок, номера или диапазоны: feature_1,feature_2 / 1,2 / 0-50")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, help="Куда сохранить графики и таблицы")
    parser.add_argument("--target-col", default=DEFAULT_TARGET_COL, help="Имя target-колонки. Поставьте пустую строку, если target нет")
    parser.add_argument("--index-cols", default=",".join(DEFAULT_INDEX_COLS), help="Колонки, которые не считать признаками")
    parser.add_argument("--top-n-values", type=int, default=20, help="Сколько самых частых значений показывать на графике")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        raise FileNotFoundError(f"Не найден CSV: {csv_path}")

    train_df = pd.read_csv(csv_path)
    compare_df = None
    if args.compare_csv:
        compare_path = Path(args.compare_csv)
        if not compare_path.exists():
            raise FileNotFoundError(f"Не найден compare CSV: {compare_path}")
        compare_df = pd.read_csv(compare_path)

    target_col = args.target_col.strip() or None
    index_cols = {c.strip() for c in args.index_cols.split(",") if c.strip()}
    exclude = set(index_cols)
    if target_col:
        exclude.add(target_col)

    features = parse_feature_spec(args.features, train_df.columns, exclude=exclude)
    if not features:
        raise ValueError("Не выбрано ни одного признака. Проверьте --features и имена колонок.")

    print(f"CSV: {csv_path}")
    print(f"Rows/cols: {train_df.shape}")
    print(f"Selected features: {len(features)}")
    print(f"Output dir: {out_dir}")

    summary = plot_all_features(
        train_df=train_df,
        features=features,
        out_dir=out_dir,
        target_col=target_col,
        compare_df=compare_df,
        top_n_values=args.top_n_values,
    )

    summary_path = out_dir / "feature_distribution_summary.csv"
    suspicious_path = out_dir / "suspicious_features.csv"
    summary.to_csv(summary_path, index=False)

    if "flags" in summary.columns:
        suspicious = summary[summary["flags"].fillna("") != ""].copy()
        suspicious.to_csv(suspicious_path, index=False)
        print(f"Suspicious features: {len(suspicious)} -> {suspicious_path}")

    print(f"Summary saved: {summary_path}")
    print("Done.")


if __name__ == "__main__":
    main()
