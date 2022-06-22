"""run module."""

from io import BytesIO
from typing import Iterator
from cosmian_lib_sgx import Enclave

import pandas as pd

def input_reader(datas: Iterator[BytesIO]) -> Iterator[pd.DataFrame]:
    """Transform input data bytes to pandas DataFrame."""
    for data in datas:  # type: BytesIO
        yield pd.read_csv(data)

def main() -> int:
    """Entrypoint of your code."""
    with Enclave() as enclave:
        # import your ciphered module normally
        import secret_module
        
        # convert input data bytes from Data Providers
        datas_0: Iterator[pd.DataFrame] = input_reader(enclave.read(0))
        data_0: pd.DataFrame = next(datas_0)

        # apply your secret function coded by the Code Provider
        df_result = secret_module.cross_tabulation(data_0, ("child", "woman", "man"))

        # convert output result
        result: bytes = df_result.to_csv(index_label='class').encode("utf-8")

        # write result for Result Consumers
        enclave.write(result)

    return 0

if __name__ == "__main__":
    main()
    