# Beast Mode Formula Examples

Quick reference for common calculations in Domo beast modes. All column names must be wrapped in backticks.

## Financial Calculations

### Profit Margin

```sql
(`revenue` - `cost`) / `revenue` * 100
```

Returns: DECIMAL (percentage)

### Markup

```sql
(`selling_price` - `cost_price`) / `cost_price` * 100
```

Returns: DECIMAL

### Return on Investment (ROI)

```sql
(`profit` / `investment`) * 100
```

Returns: DECIMAL

### Gross Profit

```sql
`revenue` - `cost_of_goods_sold`
```

Returns: LONG or DECIMAL

### Net Income

```sql
`revenue` - `total_expenses`
```

Returns: DECIMAL

---

## String Operations

### Full Name (Concatenation)

```sql
CONCAT(`first_name`, ' ', `last_name`)
```

Returns: STRING

### Email with Domain

```sql
CONCAT(`username`, '@', `domain`)
```

Returns: STRING

### Uppercase Status

```sql
UPPER(`status`)
```

Returns: STRING

### Extract Area Code from Phone

```sql
SUBSTRING(`phone_number`, 1, 3)
```

Returns: STRING

### Remove Whitespace

```sql
TRIM(`column_name`)
```

Returns: STRING

### Replace Values

```sql
REPLACE(`product_name`, 'Old', 'New')
```

Returns: STRING

---

## Aggregates & Counting

### Total Revenue

```sql
SUM(`amount`)
```

Returns: LONG or DECIMAL

### Average Order Value

```sql
AVG(`order_amount`)
```

Returns: DECIMAL

### Unique Customers

```sql
COUNT(DISTINCT `customer_id`)
```

Returns: LONG

### Product Count

```sql
COUNT(`product_id`)
```

Returns: LONG

### Highest Price

```sql
MAX(`price`)
```

Returns: DECIMAL

### Lowest Price

```sql
MIN(`price`)
```

Returns: DECIMAL

---

## Date Calculations

### Days Since Signup

```sql
DATE_DIFF(NOW(), `signup_date`)
```

Returns: LONG (days)

### Extract Year from Date

```sql
YEAR(`order_date`)
```

Returns: LONG

### Extract Month

```sql
MONTH(`created_date`)
```

Returns: LONG

### Extract Day

```sql
DAY(`date`)
```

Returns: LONG

### Quarter from Date

```sql
QUARTER(`date`)
```

Returns: LONG (1-4)

### Format Date as String

```sql
DATE_FORMAT(`date`, '%Y-%m-%d')
```

Returns: STRING (format: YYYY-MM-DD)

### Days Between Two Dates

```sql
DATE_DIFF(`end_date`, `start_date`)
```

Returns: LONG

---

## Conditional Logic (CASE WHEN)

### Status to Number

```sql
CASE 
  WHEN `status` = 'active' THEN 1 
  WHEN `status` = 'inactive' THEN 0 
  ELSE NULL 
END
```

Returns: LONG

### Sales Category

```sql
CASE 
  WHEN `amount` > 10000 THEN 'High'
  WHEN `amount` > 5000 THEN 'Medium'
  ELSE 'Low'
END
```

Returns: STRING

### Commission Calculation

```sql
CASE 
  WHEN `sale_amount` > 50000 THEN `sale_amount` * 0.1
  WHEN `sale_amount` > 25000 THEN `sale_amount` * 0.07
  ELSE `sale_amount` * 0.05
END
```

Returns: DECIMAL

### Priority Flag

```sql
CASE 
  WHEN `days_overdue` > 30 THEN 'Critical'
  WHEN `days_overdue` > 14 THEN 'High'
  WHEN `days_overdue` > 0 THEN 'Medium'
  ELSE 'On Time'
END
```

Returns: STRING

---

## Complex: Conditional Aggregates

### Sales Total for Completed Orders Only

```sql
SUM(CASE WHEN `status` = 'completed' THEN `amount` ELSE 0 END)
```

Returns: DECIMAL
Use when: You need a total but only for certain rows

### Count of Active Users

```sql
COUNT(CASE WHEN `is_active` = 1 THEN 1 END)
```

Returns: LONG

### Average Revenue for Specific Region

```sql
AVG(CASE WHEN `region` = 'North America' THEN `revenue` ELSE NULL END)
```

Returns: DECIMAL

### Percentage of Orders Completed

```sql
COUNT(CASE WHEN `status` = 'completed' THEN 1 END) / COUNT(*) * 100
```

Returns: DECIMAL

---

## Math Operations

### Absolute Value (Always Positive)

```sql
ABS(`variance`)
```

Returns: LONG or DECIMAL

### Round to 2 Decimals

```sql
ROUND(`price`, 2)
```

Returns: DECIMAL

### Round Up

```sql
CEILING(`value`)
```

Returns: LONG

### Round Down

```sql
FLOOR(`value`)
```

Returns: LONG

### Square Root

```sql
SQRT(`area`)
```

Returns: DECIMAL

### Power (Exponent)

```sql
POWER(`base`, 2)
```

Returns: DECIMAL

---

## Null Handling (COALESCE)

### Use Default if NULL

```sql
COALESCE(`discount_amount`, 0)
```

Returns: Same as input (NULL becomes 0)

### First Non-Null Value

```sql
COALESCE(`billing_address`, `shipping_address`, 'No Address')
```

Returns: STRING

---

## Performance Tips

1. **Keep it simple** — Deeply nested CASE statements are harder to debug
2. **Test in UI first** — Validate your formula in Domo's formula editor before generating curl
3. **Use COALESCE for nulls** — Prevents calculation errors from NULL values
4. **Break complex formulas** — Create multiple beast modes and reference them instead of nesting
5. **Wrap column names in backticks** — Always: ``column_name``, never `column_name`

---

## Common Mistakes


| Mistake                            | Problem             | Fix                                     |
| ---------------------------------- | ------------------- | --------------------------------------- |
| `SUM(revenue)`                     | Missing backticks   | `SUM(`revenue`)`                        |
| `CASE status = 'active'`           | Wrong syntax        | `CASE WHEN status = 'active'`           |
| `DATE_DIFF(date1 date2)`           | Missing comma       | `DATE_DIFF(date1, date2)`               |
| `CONCAT(first middle last)`        | Missing separators  | `CONCAT(first, ' ', middle, ' ', last)` |
| `COUNT(id)` (returns wrong result) | Should use DISTINCT | `COUNT(DISTINCT id)`                    |


---

## Testing Your Formula

Before running the curl command:

1. **Check syntax** — Is every column wrapped in backticks?
2. **Verify column names** — Do they match the schema exactly?
3. **Test in Domo UI** — Go to Card → Edit → Formula to test
4. **Use validation endpoint** — POST to `/query/v1/functions/validateFormulas`

If validation says `"status": "VALID"`, you're safe to run the curl command.