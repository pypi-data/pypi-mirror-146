# Guidelines 

## Instalation
To install this package use pip as following 

`pip install rst-tools`

## Usage 

```python
import pandas as pd
from rst_tools.roughsets import RoughSets as RST
from rst_tools.roughsets import QuickReduct as QR

df = pd.read_csv("YOUR/FILE.csv")
conditional_attributes = list(df.column.values)
decision_attribute = conditional_attributes[-1]
del conditional_attributes[-1]

roughsets = RST(df)

'''....'''
```