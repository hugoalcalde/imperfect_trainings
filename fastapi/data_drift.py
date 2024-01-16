import pandas as pd 
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from evidently.options import ColorOptions
from evidently.test_suite import TestSuite
from evidently.tests import *



reference_data = pd.read_csv("reference_database.csv")
current_data = pd.read_csv("qa_database.csv")

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference_data, current_data=current_data)
report.save_html('report.html')

data_quality_column_tests = TestSuite(tests=[
    TestColumnValueMin(column_name='mean'),
    TestColumnValueMax(column_name='mean'),
    TestColumnValueMean(column_name='mean'),
    TestColumnValueMedian(column_name='mean'),
    TestColumnValueStd(column_name='mean'),
    TestValueRange(column_name='mean'),
    TestColumnQuantile(column_name='mean', quantile=0.25), 

    TestColumnValueMin(column_name='image_x'),
    TestColumnValueMax(column_name='image_x'),
    TestColumnValueMean(column_name='image_x'),
    TestColumnValueMedian(column_name='image_x'),
    TestColumnValueStd(column_name='image_x'),
    TestValueRange(column_name='image_x'),
    TestColumnQuantile(column_name='image_x', quantile=0.25), 

    TestColumnValueMin(column_name='image_y'),
    TestColumnValueMax(column_name='image_y'),
    TestColumnValueMean(column_name='image_y'),
    TestColumnValueMedian(column_name='image_y'),
    TestColumnValueStd(column_name='image_y'),
    TestValueRange(column_name='image_y'),
    TestColumnQuantile(column_name='image_y', quantile=0.25)

])

data_quality_column_tests.run(reference_data=reference_data, current_data=current_data)
data_quality_column_tests.save_html('report_tests.html')