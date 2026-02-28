# tests/test_etl.py
import os
import pandas as pd
from etl import extract_data, transform_data, load_data


def test_extract_data_reads_csv(tmp_path):
    # Arrange: create a temporary CSV file
    csv_path = tmp_path / "input.csv"
    df_original = pd.DataFrame(
        {
            "employee_id": [1, 2],
            "salary": [3000.0, 4000.0],
        }
    )
    df_original.to_csv(csv_path, index=False)

    # Act
    df_extracted = extract_data(csv_path)

    # Assert
    assert df_extracted is not None
    assert list(df_extracted.columns) == ["employee_id", "salary"]
    assert df_extracted.shape == (2, 2)
    pd.testing.assert_frame_equal(df_extracted, df_original)


def test_transform_data_adds_tax_and_net_salary():
    # Arrange: build a DataFrame with some NaNs and valid rows
    df_raw = pd.DataFrame(
        {
            "employee_id": [1, 2, 3],
            "salary": [3000.0, None, 5000.0],  # Row 2 should be dropped
        }
    )

    # Act
    df_transformed = transform_data(df_raw)

    # Assert basic shape: one row with NaN should be removed
    assert df_transformed is not None
    assert df_transformed.shape[0] == 2
    assert "tax" in df_transformed.columns
    assert "net_salary" in df_transformed.columns

    # Check tax and net_salary calculations (10% tax)
    for _, row in df_transformed.iterrows():
        expected_tax = row["salary"] * 0.1
        expected_net = row["salary"] - expected_tax
        assert abs(row["tax"] - expected_tax) < 1e-6
        assert abs(row["net_salary"] - expected_net) < 1e-6


def test_load_data_writes_csv(tmp_path):
    # Arrange: create a simple DataFrame
    df = pd.DataFrame(
        {
            "employee_id": [1, 2],
            "salary": [3000.0, 4000.0],
            "tax": [300.0, 400.0],
            "net_salary": [2700.0, 3600.0],
        }
    )
    output_path = tmp_path / "output.csv"

    # Act
    load_data(df, output_path)

    # Assert: file exists and contents match
    assert output_path.exists()
    df_loaded = pd.read_csv(output_path)
    pd.testing.assert_frame_equal(df_loaded, df)


def test_etl_end_to_end(tmp_path):
    """
    Optional: end-to-end test of the whole etl_process.
    This uses a temp input file and checks the output file is created
    and contains the expected columns.
    """
    from etl import etl_process  # imported here to avoid circular imports

    # Arrange input
    input_path = tmp_path / "input_data.csv"
    output_path = tmp_path / "output_data.csv"

    df_input = pd.DataFrame(
        {
            "employee_id": [1, 2],
            "salary": [3000.0, 4500.0],
        }
    )
    df_input.to_csv(input_path, index=False)

    # Act
    etl_process(str(input_path), str(output_path))

    # Assert
    assert output_path.exists()
    df_output = pd.read_csv(output_path)
    # Should have tax & net_salary columns
    assert "tax" in df_output.columns
    assert "net_salary" in df_output.columns
    assert df_output.shape[0] == 2