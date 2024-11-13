import json
import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import get_data_from_excel

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "reports.log"),
    filemode="w",
    format="%(asctime)s: %(name)s: %(levelname)s: %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "report.json")


def report(filename=PATH):
    """Decorator create report file."""

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            json_data = json.dumps(result)
            with open(filename, "w") as file:
                json.dump(json_data, file)
            return result

        return wrapper

    return my_decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Function get sum of spending by category."""
    if date is None:
        return []
    try:
        date_format = "%d.%m.%Y"
        end_date = datetime.strptime(date, date_format)
        start_date = end_date - relativedelta(months=3)
    except ValueError:
        return "Неверный формат данных"

    current_transactions = []
    for index, transaction in transactions.iterrows():
        if not isinstance(transaction["Дата платежа"], str):
            continue
        transaction_date = datetime.strptime(transaction["Дата платежа"], date_format)
        if transaction["Категория"] == category and start_date <= transaction_date <= end_date:
            current_transactions.append(transaction.to_dict())
    logger.debug(f"Correct returned spending by category {category}")
    return current_transactions


df = get_data_from_excel("../data/operations.xlsx")
if __name__ == "__main__":
    print(spending_by_category(df, "Супермаркеты", "08.10.2021"))
