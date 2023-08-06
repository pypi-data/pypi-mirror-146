# import pandas as pd
# df = pd.read_csv('D:/WS/VSCode/waveletai/tests/dataset_init/csv文件夹/devices_curvy.csv')
# df.to_parquet('output.parquet')
import pyarrow.parquet as pq
# table = pd.read_parquet('output.parquet')
#
# pq.read_table('output.parquet')
# table = pq.read_schema("D:/VISIO/AI平台/02 研发/02 数据/x_train.parquet")
parquet_file = pq.ParquetFile("D:/VISIO/AI平台/02 研发/02 数据/x_train.parquet")
print(parquet_file.metadata)
# print(parquet_file.read_row_group(0))
# first_ten_rows = next(parquet_file.iter_batches(batch_size = 10))
# print(first_ten_rows)
# df = parquet_file.Table.from_batches([first_ten_rows]).to_pandas()
# print(df)
# print(table.metadata)



# from pyarrow.parquet import ParquetFile
# import pyarrow as pa
#
# pf = ParquetFile('file_name.pq')
# first_ten_rows = next(pf.iter_batches(batch_size = 10))
# df = pa.Table.from_batches([first_ten_rows]).to_pandas()