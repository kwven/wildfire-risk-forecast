# Fire Risk Prediction 2023 - Final Report Draft

## Study Area
Morocco + Western Sahara, using a regular grid over the bounding box.

## Data Sources
- NASA FIRMS VIIRS_SNPP_SP active fire detections
- MODIS MOD13Q1.061 250m 16-day NDVI from AppEEARS
- NOAA weather integration remains optional and was not required for the first baseline

## Target
Binary target: fire detected in the next 7 days for a grid cell.

## Best Available Model In This Run
- Model: temporal_cnn
- Threshold: 0.9696
- Precision: 0.4245
- Recall: 0.3305
- F1: 0.3716
- ROC AUC: 0.9063
- PR AUC: 0.3313
- Alerts: 1901

## Critical Interpretation
High ROC AUC can coexist with low precision because fire-risk positives are rare. PR AUC, precision, recall, and alert volume should guide operational interpretation.

## Main Limitations
- FIRMS active fire detections are a proxy target, not confirmed burned area.
- The rectangular grid includes non-burnable and sparse-vegetation areas unless filtered.
- Weather, drought, land cover, elevation, and human activity features are still missing.
- Results are from one year only, so temporal generalization is not proven.

## Recommended Next Improvements
1. Add weather or gridded climate data, preferably ERA5-Land or CHIRPS if NOAA station coverage is weak.
2. Add land-cover and elevation/topography variables.
3. Extend the dataset to multiple years and test on a future year.
4. Evaluate Morocco and Western Sahara separately.
5. Treat predictions as risk scores and choose thresholds based on the intended use case.

## Generated Files
- Model comparison: /content/drive/MyDrive/fire-risk-project/outputs/reports/model_comparison_2023.csv
- Monthly summary: /content/drive/MyDrive/fire-risk-project/outputs/reports/monthly_prediction_summary_2023.csv
- Risk probability map: /content/drive/MyDrive/fire-risk-project/outputs/figures/selected_model_risk_probability_map.png
- Alert map: /content/drive/MyDrive/fire-risk-project/outputs/figures/selected_model_alert_map.png