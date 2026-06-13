# Submissions report (`submissions_2`)

Скоры переписаны только с leaderboard-скриншотов с именами `submission_*.csv`. Скриншоты из переписки/чата без имени файла сюда намеренно не добавлены.

Пути кликабельные и рассчитаны на то, что этот файл лежит рядом с csv в `submissions_2/`.

| Submission | Path | Private | Public | Local CV / OOF | Краткое описание |
|---|---:|---:|---:|---:|---|
| `submission_blend_logistic_stacker_rank.csv` | [./submission_blend_logistic_stacker_rank.csv](./submission_blend_logistic_stacker_rank.csv) | 0.68693 | 0.65636 | 0.715784 | Rank-space logistic stacker over top OOF base predictions; meta LogisticRegression(C=0.35, class_weight=balanced). Validation is less strict than base OOF because stacker is selected on OOF meta-features. |
| `submission_blend_logistic_stacker_probability.csv` | [./submission_blend_logistic_stacker_probability.csv](./submission_blend_logistic_stacker_probability.csv) | 0.68882 | 0.65974 | 0.716513 | Probability-space logistic stacker over top OOF base predictions; meta LogisticRegression(C=0.35, class_weight=balanced). |
| `submission_blend_random_search_prob.csv` | [./submission_blend_random_search_prob.csv](./submission_blend_random_search_prob.csv) | 0.68497 | 0.65481 | 0.717250 | Dirichlet random-search probability blend over top base models; weights optimized by OOF ROC-AUC. |
| `submission_blend_manual_descending_probability.csv` | [./submission_blend_manual_descending_probability.csv](./submission_blend_manual_descending_probability.csv) | 0.68143 | 0.65073 | 0.715775 | Manual descending probability blend: larger weights for higher-OOF models, small nonzero weights for diversity. |
| `submission_blend_auc_weighted_rank.csv` | [./submission_blend_auc_weighted_rank.csv](./submission_blend_auc_weighted_rank.csv) | 0.68298 | 0.65210 | 0.715239 | Rank blend with weights proportional to max(OOF_AUC - 0.5, eps). |
| `submission_blend_auc_weighted_probability.csv` | [./submission_blend_auc_weighted_probability.csv](./submission_blend_auc_weighted_probability.csv) | 0.68436 | 0.65357 | 0.715472 | Probability blend with weights proportional to max(OOF_AUC - 0.5, eps). |
| `submission_blend_equal_rank_top.csv` | [./submission_blend_equal_rank_top.csv](./submission_blend_equal_rank_top.csv) | 0.68306 | 0.65217 | 0.715223 | Equal-weight rank blend over top base models by local OOF. |
| `submission_blend_equal_probability_top.csv` | [./submission_blend_equal_probability_top.csv](./submission_blend_equal_probability_top.csv) | 0.68443 | 0.65364 | 0.715456 | Equal-weight probability blend over top base models by local OOF. |
| `submission_catboost_linear_stack_compact.csv` | [./submission_catboost_linear_stack_compact.csv](./submission_catboost_linear_stack_compact.csv) | 0.68306 | 0.65923 | 0.709989 | CatBoost on v2_linear_stack_compact. params: iterations=3500, lr=0.03, depth=5, l2_leaf_reg=25, auto_class_weights=Balanced, early_stopping=180. |
| `submission_catboost_peak_freq_te.csv` | [./submission_catboost_peak_freq_te.csv](./submission_catboost_peak_freq_te.csv) | 0.66065 | 0.63252 | 0.705806 | CatBoost on v2_peak_freq_te. params: iterations=3500, lr=0.025, depth=6, l2_leaf_reg=18, bagging_temperature=0.6, auto_class_weights=Balanced. |
| `submission_xgb_pca_svd_stack.csv` | [./submission_xgb_pca_svd_stack.csv](./submission_xgb_pca_svd_stack.csv) | 0.68315 | 0.65670 | 0.699434 | XGBoost hist on v2_pca_svd_stack; imbalance-aware scale_pos_weight; tree booster, early stopping by fold. |
| `submission_xgb_peak_freq_te.csv` | [./submission_xgb_peak_freq_te.csv](./submission_xgb_peak_freq_te.csv) | 0.66008 | 0.63439 | 0.704309 | XGBoost hist on v2_peak_freq_te; imbalance-aware scale_pos_weight; tree booster, early stopping by fold. |
| `submission_extratrees_v2_pca_svd_stack_fullfit.csv` | [./submission_extratrees_v2_pca_svd_stack_fullfit.csv](./submission_extratrees_v2_pca_svd_stack_fullfit.csv) | 0.66211 | 0.63985 | — | Fullfit ExtraTrees on v2_pca_svd_stack. Base CV model params: n_estimators=420, min_samples_leaf=8, max_features=0.45, class_weight=balanced_subsample. |
| `submission_extratrees_v2_pca_svd_stack.csv` | [./submission_extratrees_v2_pca_svd_stack.csv](./submission_extratrees_v2_pca_svd_stack.csv) | 0.68290 | 0.65442 | 0.692331 | 5-fold CV-averaged ExtraTrees on v2_pca_svd_stack. n_estimators=420, min_samples_leaf=8, max_features=0.45, class_weight=balanced_subsample. |
| `submission_histgb_v2_pca_svd_stack_fullfit.csv` | [./submission_histgb_v2_pca_svd_stack_fullfit.csv](./submission_histgb_v2_pca_svd_stack_fullfit.csv) | 0.67588 | 0.65054 | — | Fullfit HistGradientBoosting on v2_pca_svd_stack. Base CV params: lr=0.035, max_iter=600, max_leaf_nodes=31, min_samples_leaf=80, l2=1.5, class_weight=balanced. |
| `submission_histgb_v2_pca_svd_stack.csv` | [./submission_histgb_v2_pca_svd_stack.csv](./submission_histgb_v2_pca_svd_stack.csv) | 0.67825 | 0.65383 | 0.703634 | 5-fold CV-averaged HistGradientBoosting on v2_pca_svd_stack. lr=0.035, max_iter=600, max_leaf_nodes=31, min_samples_leaf=80, l2=1.5. |
| `submission_logreg_v2_linear_stack_compact_fullfit.csv` | [./submission_logreg_v2_linear_stack_compact_fullfit.csv](./submission_logreg_v2_linear_stack_compact_fullfit.csv) | 0.66887 | 0.64811 | — | Fullfit LogisticRegression on v2_linear_stack_compact. Base CV params: StandardScaler + LogisticRegression(C=0.25, saga, L2, class_weight=balanced). |
| `submission_logreg_v2_linear_stack_compact.csv` | [./submission_logreg_v2_linear_stack_compact.csv](./submission_logreg_v2_linear_stack_compact.csv) | 0.66755 | 0.64533 | 0.694134 | 5-fold CV-averaged LogisticRegression on v2_linear_stack_compact. StandardScaler + LogisticRegression(C=0.25, saga, L2, class_weight=balanced). |
| `submission_lgb_optuna_best_fullfit.csv` | [./submission_lgb_optuna_best_fullfit.csv](./submission_lgb_optuna_best_fullfit.csv) | 0.67007 | 0.64734 | — | Fullfit LightGBM with Optuna-selected params on v2_peak_freq_te. Base OOF model: lgb_optuna_best. |
| `submission_lgb_optuna_best.csv` | [./submission_lgb_optuna_best.csv](./submission_lgb_optuna_best.csv) | 0.66834 | 0.63962 | 0.709474 | 5-fold CV-averaged LightGBM using Optuna-selected hyperparameters on v2_peak_freq_te. |
| `submission_lgb_peak_noise_downweight_fullfit.csv` | [./submission_lgb_peak_noise_downweight_fullfit.csv](./submission_lgb_peak_noise_downweight_fullfit.csv) | 0.67599 | 0.64622 | — | Fullfit LightGBM noise-downweight variant on v2_peak_freq_te. Base params: lr=0.014, num_leaves=64, min_leaf=90, ff=0.78, bagging=0.82, l2=28. |
| `submission_lgb_peak_noise_downweight.csv` | [./submission_lgb_peak_noise_downweight.csv](./submission_lgb_peak_noise_downweight.csv) | 0.67977 | 0.64575 | 0.707554 | 5-fold CV-averaged LightGBM on v2_peak_freq_te with suspicious/noisy rows downweighted. lr=0.014, leaves=64, min_leaf=90, ff=0.78, bagging=0.82, l2=28. |
| `submission_lgb_peak_goss_fullfit.csv` | [./submission_lgb_peak_goss_fullfit.csv](./submission_lgb_peak_goss_fullfit.csv) | 0.66471 | 0.64482 | — | Fullfit LightGBM GOSS on v2_peak_freq_te. Base params: boosting=goss, lr=0.014, leaves=52, min_leaf=100, ff=0.82, l2=25. |
| `submission_lgb_peak_goss.csv` | [./submission_lgb_peak_goss.csv](./submission_lgb_peak_goss.csv) | 0.67292 | 0.64295 | 0.707886 | 5-fold CV-averaged LightGBM GOSS on v2_peak_freq_te. boosting=goss, lr=0.014, leaves=52, min_leaf=100, ff=0.82, l2=25. |
| `submission_lgb_peak_dart_fullfit.csv` | [./submission_lgb_peak_dart_fullfit.csv](./submission_lgb_peak_dart_fullfit.csv) | 0.64279 | 0.61424 | — | Fullfit LightGBM DART on v2_peak_freq_te. Base params: boosting=dart, lr=0.018, leaves=48, min_leaf=120, ff=0.78, bagging=0.82, drop_rate=0.08. |
| `submission_lgb_peak_dart.csv` | [./submission_lgb_peak_dart.csv](./submission_lgb_peak_dart.csv) | 0.68889 | 0.65463 | 0.700699 | 5-fold CV-averaged LightGBM DART on v2_peak_freq_te. boosting=dart, lr=0.018, leaves=48, min_leaf=120, ff=0.78, bagging=0.82, drop_rate=0.08. |
| `submission_lgb_top500_meta_fullfit.csv` | [./submission_lgb_top500_meta_fullfit.csv](./submission_lgb_top500_meta_fullfit.csv) | 0.67400 | 0.64163 | — | Fullfit LightGBM on v2_lgb_top500_meta. Base params: lr=0.016, leaves=44, max_depth=7, min_leaf=95, ff=0.86, bagging=0.78, l2=28. |
| `submission_lgb_top500_meta.csv` | [./submission_lgb_top500_meta.csv](./submission_lgb_top500_meta.csv) | 0.66896 | 0.64581 | 0.687521 | 5-fold CV-averaged LightGBM on v2_lgb_top500_meta. lr=0.016, leaves=44, max_depth=7, min_leaf=95, ff=0.86, bagging=0.78, l2=28. |
| `submission_lgb_nodrift_top700_fullfit.csv` | [./submission_lgb_nodrift_top700_fullfit.csv](./submission_lgb_nodrift_top700_fullfit.csv) | 0.68432 | 0.64812 | — | Fullfit LightGBM on v2_nodrift_top700_engineered. Base params: lr=0.012, leaves=56, min_leaf=140, ff=0.72, bagging=0.82, l2=45. |
| `submission_lgb_nodrift_top700.csv` | [./submission_lgb_nodrift_top700.csv](./submission_lgb_nodrift_top700.csv) | 0.68146 | 0.64800 | 0.703342 | 5-fold CV-averaged LightGBM on v2_nodrift_top700_engineered. lr=0.012, leaves=56, min_leaf=140, ff=0.72, bagging=0.82, l2=45. |
| `submission_lgb_linear_stack_compact_fullfit.csv` | [./submission_lgb_linear_stack_compact_fullfit.csv](./submission_lgb_linear_stack_compact_fullfit.csv) | 0.67058 | 0.64483 | — | Fullfit LightGBM on v2_linear_stack_compact. Base params: lr=0.020, leaves=32, max_depth=6, min_leaf=110, ff=0.90, bagging=0.88, l2=15. |
| `submission_lgb_linear_stack_compact.csv` | [./submission_lgb_linear_stack_compact.csv](./submission_lgb_linear_stack_compact.csv) | 0.67531 | 0.64720 | 0.621752 | 5-fold CV-averaged LightGBM on v2_linear_stack_compact. lr=0.020, leaves=32, max_depth=6, min_leaf=110, ff=0.90, bagging=0.88, l2=15. |
| `submission_lgb_top500_engineered_fullfit.csv` | [./submission_lgb_top500_engineered_fullfit.csv](./submission_lgb_top500_engineered_fullfit.csv) | 0.68452 | 0.65402 | — | Fullfit LightGBM on top500_plus_engineered. Base params: lr=0.014, leaves=48, min_leaf=150, ff=0.60, bagging=0.82, l2=55. |
| `submission_lgb_top500_engineered.csv` | [./submission_lgb_top500_engineered.csv](./submission_lgb_top500_engineered.csv) | 0.69074 | 0.65790 | 0.702909 | 5-fold CV-averaged LightGBM on top500_plus_engineered. lr=0.014, leaves=48, min_leaf=150, ff=0.60, bagging=0.82, l2=55. |
| `submission_lgb_pca_svd_stack_fullfit.csv` | [./submission_lgb_pca_svd_stack_fullfit.csv](./submission_lgb_pca_svd_stack_fullfit.csv) | 0.66522 | 0.64041 | — | Fullfit LightGBM on v2_pca_svd_stack. Base params: lr=0.018, leaves=40, max_depth=7, min_leaf=130, ff=0.85, bagging=0.88, l2=18. |
| `submission_lgb_pca_svd_stack.csv` | [./submission_lgb_pca_svd_stack.csv](./submission_lgb_pca_svd_stack.csv) | 0.67078 | 0.64267 | 0.655215 | 5-fold CV-averaged LightGBM on v2_pca_svd_stack. lr=0.018, leaves=40, max_depth=7, min_leaf=130, ff=0.85, bagging=0.88, l2=18. |
| `submission_lgb_peak_regularized.csv` | [./submission_lgb_peak_regularized.csv](./submission_lgb_peak_regularized.csv) | 0.68010 | 0.64481 | 0.706058 | 5-fold CV-averaged regularized LightGBM on v2_peak_freq_te. lr=0.014, leaves=64, min_leaf=90, ff=0.78, bagging=0.82, l2=22. |
| `submission_lgb_peak_regularized_fullfit.csv` | [./submission_lgb_peak_regularized_fullfit.csv](./submission_lgb_peak_regularized_fullfit.csv) | 0.67732 | 0.64396 | — | Fullfit regularized LightGBM on v2_peak_freq_te. Base params: lr=0.014, leaves=64, min_leaf=90, ff=0.78, bagging=0.82, l2=22. |
| `submission_lgb_peak_deeper.csv` | [./submission_lgb_peak_deeper.csv](./submission_lgb_peak_deeper.csv) | 0.66161 | 0.62972 | 0.692214 | 5-fold CV-averaged deeper LightGBM on v2_peak_freq_te. lr=0.010, leaves=96, max_depth=9, min_leaf=70, ff=0.70, bagging=0.80, l2=35. |
| `submission_lgb_peak_deeper_fullfit.csv` | [./submission_lgb_peak_deeper_fullfit.csv](./submission_lgb_peak_deeper_fullfit.csv) | 0.66411 | 0.63475 | — | Fullfit deeper LightGBM on v2_peak_freq_te. Base params: lr=0.010, leaves=96, max_depth=9, min_leaf=70, ff=0.70, bagging=0.80, l2=35. |

## Top by private score

1. [`submission_lgb_top500_engineered.csv`](./submission_lgb_top500_engineered.csv) — private `0.69074`, public `0.65790`, local `0.702909`
2. [`submission_lgb_peak_dart.csv`](./submission_lgb_peak_dart.csv) — private `0.68889`, public `0.65463`, local `0.700699`
3. [`submission_blend_logistic_stacker_probability.csv`](./submission_blend_logistic_stacker_probability.csv) — private `0.68882`, public `0.65974`, local `0.716513`
4. [`submission_blend_logistic_stacker_rank.csv`](./submission_blend_logistic_stacker_rank.csv) — private `0.68693`, public `0.65636`, local `0.715784`
5. [`submission_blend_random_search_prob.csv`](./submission_blend_random_search_prob.csv) — private `0.68497`, public `0.65481`, local `0.717250`
6. [`submission_lgb_top500_engineered_fullfit.csv`](./submission_lgb_top500_engineered_fullfit.csv) — private `0.68452`, public `0.65402`, local `—`
7. [`submission_blend_equal_probability_top.csv`](./submission_blend_equal_probability_top.csv) — private `0.68443`, public `0.65364`, local `0.715456`
8. [`submission_blend_auc_weighted_probability.csv`](./submission_blend_auc_weighted_probability.csv) — private `0.68436`, public `0.65357`, local `0.715472`
9. [`submission_lgb_nodrift_top700_fullfit.csv`](./submission_lgb_nodrift_top700_fullfit.csv) — private `0.68432`, public `0.64812`, local `—`
10. [`submission_xgb_pca_svd_stack.csv`](./submission_xgb_pca_svd_stack.csv) — private `0.68315`, public `0.65670`, local `0.699434`
11. [`submission_blend_equal_rank_top.csv`](./submission_blend_equal_rank_top.csv) — private `0.68306`, public `0.65217`, local `0.715223`
12. [`submission_catboost_linear_stack_compact.csv`](./submission_catboost_linear_stack_compact.csv) — private `0.68306`, public `0.65923`, local `0.709989`
13. [`submission_blend_auc_weighted_rank.csv`](./submission_blend_auc_weighted_rank.csv) — private `0.68298`, public `0.65210`, local `0.715239`
14. [`submission_extratrees_v2_pca_svd_stack.csv`](./submission_extratrees_v2_pca_svd_stack.csv) — private `0.68290`, public `0.65442`, local `0.692331`
15. [`submission_lgb_nodrift_top700.csv`](./submission_lgb_nodrift_top700.csv) — private `0.68146`, public `0.64800`, local `0.703342`

## Notes

- `*_fullfit.csv` обучались на всём train после CV-подбора числа итераций/настроек; собственного OOF-скора у fullfit-файла нет, поэтому в таблице стоит `—`.

- Локальные OOF-скоры для v2-моделей могли быть оптимистичны из-за старой схемы feature engineering; они оставлены только как историческая справка.

- Самый полезный эмпирический сигнал: CV-average часто лучше fullfit, а сильные приросты появляются от блендов разнородных моделей.
