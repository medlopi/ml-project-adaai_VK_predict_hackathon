# Submissions v3 — leaderboard scores

Сортировка по `Private Score` по убыванию. Пути кликабельные при размещении файла в директории `submissions_2/` рядом с CSV.

| # | Submission | Private | Public | Gap private-public | Краткое описание |
|---:|---|---:|---:|---:|---|
| 1 | [`./submission_blend_logistic_stacker_v3.csv`](./submission_blend_logistic_stacker_v3.csv) | 0.68943 | 0.67117 | +0.01826 | Logistic stacker over model OOF predictions; meta-model combines probability predictions. |
| 2 | [`./submission_lgb_dart_v3.csv`](./submission_lgb_dart_v3.csv) | 0.68927 | 0.66682 | +0.02245 | LightGBM DART variant; dropout boosting, useful diversity vs standard GBDT. |
| 3 | [`./submission_blend_greedy_oof_v3.csv`](./submission_blend_greedy_oof_v3.csv) | 0.68891 | 0.66847 | +0.02044 | Greedy OOF blend; iteratively adds models/weights by local OOF AUC. |
| 4 | [`./submission_lgb_deeper_v3.csv`](./submission_lgb_deeper_v3.csv) | 0.68765 | 0.66558 | +0.02207 | LightGBM deeper trees; larger leaves/depth than regularized baseline. |
| 5 | [`./submission_blend_equal_probability_topk_v3.csv`](./submission_blend_equal_probability_topk_v3.csv) | 0.68567 | 0.66475 | +0.02092 | Equal probability blend over top-k strongest/diverse model predictions. |
| 6 | [`./submission_blend_auc_weighted_topk_v3.csv`](./submission_blend_auc_weighted_topk_v3.csv) | 0.68522 | 0.66429 | +0.02093 | OOF-AUC weighted blend over top-k model predictions. |
| 7 | [`./submission_flaml_automl_v3.csv`](./submission_flaml_automl_v3.csv) | 0.68439 | 0.66971 | +0.01468 | FLAML AutoML model/pipeline selected under time budget. |
| 8 | [`./submission_blend_cv_weight_search_v3.csv`](./submission_blend_cv_weight_search_v3.csv) | 0.68419 | 0.66892 | +0.01527 | CV weight-search blend; weights optimized by OOF/CV objective. |
| 9 | [`./submission_lgb_goss_v3.csv`](./submission_lgb_goss_v3.csv) | 0.68259 | 0.66569 | +0.01690 | LightGBM GOSS boosting variant. |
| 10 | [`./submission_blend_equal_rank_topk_v3.csv`](./submission_blend_equal_rank_topk_v3.csv) | 0.68246 | 0.66121 | +0.02125 | Equal rank blend over top-k model predictions. |
| 11 | [`./submission_xgb_depth4_v3.csv`](./submission_xgb_depth4_v3.csv) | 0.67824 | 0.65558 | +0.02266 | XGBoost histogram/tree model, max_depth≈4. |
| 12 | [`./submission_xgb_depth6_regularized_v3.csv`](./submission_xgb_depth6_regularized_v3.csv) | 0.67548 | 0.65011 | +0.02537 | XGBoost histogram/tree model, depth≈6 with stronger regularization. |
| 13 | [`./submission_lgb_regularized_v3.csv`](./submission_lgb_regularized_v3.csv) | 0.67524 | 0.65554 | +0.01970 | Regularized LightGBM GBDT baseline. |
| 14 | [`./submission_lgb_small_leaves_v3.csv`](./submission_lgb_small_leaves_v3.csv) | 0.67465 | 0.65394 | +0.02071 | LightGBM with smaller leaves / more conservative tree complexity. |
| 15 | [`./submission_random_forest_balanced_v3.csv`](./submission_random_forest_balanced_v3.csv) | 0.67129 | 0.65687 | +0.01442 | Balanced RandomForest / class-weighted bagged trees. |
| 16 | [`./submission_catboost_depth6_v3.csv`](./submission_catboost_depth6_v3.csv) | 0.66424 | 0.64420 | +0.02004 | CatBoost depth≈6 model. |
| 17 | [`./submission_hist_gradient_boosting_v3.csv`](./submission_hist_gradient_boosting_v3.csv) | 0.66381 | 0.64955 | +0.01426 | sklearn HistGradientBoostingClassifier. |
| 18 | [`./submission_logreg_saga_l1_sparse_v3.csv`](./submission_logreg_saga_l1_sparse_v3.csv) | 0.66191 | 0.63354 | +0.02837 | Sparse Logistic Regression with SAGA solver and L1 penalty. |
| 19 | [`./submission_logreg_saga_l2_v3.csv`](./submission_logreg_saga_l2_v3.csv) | 0.66181 | 0.63359 | +0.02822 | Logistic Regression with SAGA solver and L2 penalty. |
| 20 | [`./submission_catboost_depth4_ordered_v3.csv`](./submission_catboost_depth4_ordered_v3.csv) | 0.65721 | 0.64147 | +0.01574 | CatBoost ordered boosting, depth≈4. |
| 21 | [`./submission_extra_trees_v3.csv`](./submission_extra_trees_v3.csv) | 0.64891 | 0.64376 | +0.00515 | ExtraTrees ensemble. |
| 22 | [`./submission_mlp_quantile_v3.csv`](./submission_mlp_quantile_v3.csv) | 0.62135 | 0.61180 | +0.00955 | MLP neural network on quantile/scaled features. |
| 23 | [`./submission_sgd_modified_huber_v3.csv`](./submission_sgd_modified_huber_v3.csv) | 0.61849 | 0.58620 | +0.03229 | SGDClassifier with modified_huber loss. |
| 24 | [`./submission_lgb_rf_v3.csv`](./submission_lgb_rf_v3.csv) | 0.57981 | 0.57035 | +0.00946 | LightGBM random-forest boosting mode. |

## Быстрые выводы

- Лучший private score: `0.68943` у [`./submission_blend_logistic_stacker_v3.csv`](./submission_blend_logistic_stacker_v3.csv).
- Топ держат `logistic stacker`, `LightGBM DART`, `greedy OOF blend` и `deeper LightGBM`.
- Бленды дают прирост, но не все: `logistic stacker` и `greedy OOF` лучше простых equal/weighted top-k blend.
- FLAML даёт сильный одиночный результат и хороший public, поэтому его стоит оставлять в следующих блендах.
- Слабые/опасные для бленда кандидаты: `lgb_rf`, `sgd_modified_huber`, `mlp_quantile`; их лучше не включать без проверки корреляций/OOF-веса.
