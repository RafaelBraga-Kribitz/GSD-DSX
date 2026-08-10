# COMPLETE DATA INPUT TYPE INVENTORY

**All distinct patterns extracted from 4 chart catalogue screenshots**

---

## MASTER TABLE

| ID | Name | Signature | Cols | Pattern Example | Notes |
|----|------|-----------|------|-----------------|-------|
| IT001 | Two Column Numeric Simple | [numeric, numeric] | 2 | X: [1,2,3] \| Y: [30,34,38] | Basic XY scatter/line |
| IT002 | Range Range Dual Numeric | [range, numeric, numeric] | 3 | 0-2: 30,45 \| 2-4: 34,80 \| 4-6: 38,60 | Range bins with two series |
| IT003 | Three Column Numeric Series | [numeric, numeric, numeric] | 3 | 0-2: 30, 45 \| 2-4: 34, 80 | Three columns all numeric |
| IT004 | Single Value | [numeric] | 1 | 60 | Single column single value |
| IT005 | Category Single Numeric | [category, numeric] | 2 | A: 60 | One category, one value |
| IT006 | Year Range Pivot | [year, year, ...] | 3 | 2010: B,C,rows \| 2015: B,C,rows | Years as column headers |
| IT007 | Category Percentage Simple | [category, percentage] | 2 | A: 32% \| B: 40% \| C: 28% | Categories with percent values |
| IT008 | Range Category Numeric | [range, category, numeric] | 3 | 2-4: A,34 \| 4-6: B,38 | Range with category and value |
| IT009 | Event Time Mapping | [event, datetime] | 2 | Event A: 1-4-2015 \| Event B: 10-4-2015 \| Event C: 12-4-2015 | Events with associated dates |
| IT010 | Location Value Mapping | [location, numeric] | 2 | Location A: 14 \| Location B: 6 \| Location C: 15 | Geographic or spatial values |
| IT011 | Demographic Split Female Male | [age_group, female, male] | 3 | 10-20: 30,28 \| 20-30: 34,22 \| 30-40: 38,26 | Age/demographic with gender split |
| IT012 | Three Dimensional XYZ | [numeric, numeric, numeric] | 3 | X: 1 \| Y: 10 \| Z: 30 \| (row repeated) | True 3D coordinates |
| IT013 | Three Column with Index Variant | [index, numeric, numeric] | 3 | 1: 10, - \| 2: 34, 14 \| 3: 38, 12 | Index with two numeric series |
| IT014 | Date Range Interval Start End | [start_date, end_date] | 2 | Start: 1-4-2015 \| End: 6-4-2015 \| Start: 10-4-2015 \| End: 18-4-2015 | Time intervals |
| IT015 | Four Column with Year Labels | [label, year, year, ...] | 4 | Y₁, Y₂, X \| 2010: C,C,- \| 2005: C,A,A | Multiple year columns with labels |
| IT016 | Percentage Composition Two Part | [category, percent, percent] | 3 | A: 30%, 28% \| B: 34%, 32% \| C: 26%, 24% | Parts of a whole, two dimensions |
| IT017 | OHLC Financial Open High Low Close | [day, lower, close, open, upper] | 5 | day 1: $10,$20,$60,$70 \| day 2: $25,$30,$45,$65 | Stock/OHLC candlestick data |
| IT018 | Day Time Series Multiple Periods | [day, period1, period2, period3, period4] | 5 | day 1: $10,$20,$60,$70 \| day 2: $25,$30,$45,$65 | Multiple time periods per day |
| IT019 | Single Column Value Only | [numeric] | 1 | Y: 510 | One value, single column |
| IT020 | Category Percentage Triple | [category, percent, percent, percent] | 4 | X: 10%, 48%, 42% \| Y: 42%, 38%, 20% \| Z: 24%, 36%, 40% | Three-part composition |
| IT021 | Numeric Matrix 3x3 | [category, numeric, numeric, numeric] | 4 | D: 12,34,12 \| E: 0,26,34 \| F: 24,36,40 | 3x3 or larger grid |
| IT022 | Size Allocation with Percentages | [item, size, numeric, percent_a, percent_b] | 5 | Pie 1: 2,100,65%,35% \| Pie 2: 4,200,50%,50% \| Pie 3: 6,400,80%,20% | Hierarchical sizing with splits |
| IT023 | Percentage Parts Simple Two Col | [category, part_a, part_b] | 3 | A: 65%, 35% \| B: 50%, 50% \| C: 80%, 20% | Two-part percentage split |
| IT024 | Ordered Categorical Four Level | [order, level_1, level_2, level_3] | 4 | 1: Fruit, Citrus, Orange \| 2: Fruit, Citrus, Lemon \| 3: Meat, Pork, Chop | Hierarchical taxonomy with order |
| IT025 | Numeric Value Simple | [numeric] | 1 | -50 or 230 | Single numeric value |
| IT026 | Category Numeric Simple Two Col | [category, numeric] | 2 | A: 14 \| B: 16 \| C: 12 | Basic category-value pair |
| IT027 | Three Column with Index Row | [index, numeric, numeric, numeric] | 4 | 1: 30, 10, - \| 2: 34, 14, (empty) \| 3: 38, 12, (empty) | Index with three numeric columns |
| IT028 | Logical Matrix Row Col Binary | [row_cat, col_cat_A, col_cat_B, col_cat_C] | 4 | Row: A, ¬A \| Col: B, W, X, ¬B, Y, Z | Logical/boolean matrix |
| IT029 | Category Index Numeric Dual | [category, numeric, numeric] | 3 | A: 30, 14 \| B: 34, 16 \| C: 38, 10 | Two numeric values per category |
| IT030 | Roman Numeral Index | [roman_index, numeric] | 2 | I: 14 \| II: 6 | Roman numerals as index |
| IT031 | Category with Four Numeric Values | [category, numeric, numeric, numeric, numeric] | 5 | A: 14, 6, 10, (varies) \| B: 16, 12, 8, (varies) | Four metrics per category |
| IT032 | Mixed Letter Label Header | [label, numeric, numeric, numeric] | 4 | Y₁, Y₂, X headers with grid values | Letter labels as column headers |
| IT033 | Category Time Period Matrix | [category, time_period, time_period, time_period] | 4 | A: [2000:C], [2005:C], [2010:-] | Categories with time period columns |
| IT034 | Two Numeric Column Paired | [numeric, numeric] | 2 | 30, 28 \| 34, 22 \| 38, 26 | Two parallel numeric series |
| IT035 | Percentage Pair with Category | [category, percent, percent] | 3 | X: 30%, 28% \| Y: 34%, 32% \| Z: 26%, 24% | Percentage pairs by category |
| IT036 | Date Start End Formatted | [start_datetime, end_datetime] | 2 | 1-4-2015 to 6-4-2015 \| 10-4-2015 to 18-4-2015 \| 12-4-2015 to 20-4-2015 | Formatted date ranges |
| IT037 | Hierarchy Level 1-2-3-4 | [order, level_1, level_2, level_3] | 4 | 1: Fruit, Citrus, Orange \| 2: Fruit, Citrus, Lemon \| 3: Meat, Pork, Chop | Multi-level categorical hierarchy |
| IT038 | X Y with Expression | [numeric, expression] | 2 | Y: 30, 14 Y₁+Y₂ \| Y: 34, 16 Y₁+Y₂ | Numeric with derived/expression column |
| IT039 | Category Numeric Expression | [category, numeric, expression] | 3 | A: 30, 14 Y₁+Y₂ | Category with value and formula |
| IT040 | Numeric Range Boundary | [numeric_min, numeric_max] | 2 | -20 to +50 (as Start/End labels) | Numeric boundary/range |

---

## COMPLETE JSON

```json
{
  "metadata": {
    "total_input_types": 40,
    "source": "4 chart catalogue screenshots",
    "created": "2026-06-23",
    "purpose": "Machine-readable data input type catalogue for deterministic chart selection"
  },
  "input_types": [
    {
      "id": "IT001",
      "name": "Two Column Numeric Simple",
      "signature": "[numeric, numeric]",
      "columns": 2,
      "example": "X: [1,2,3] | Y: [30,34,38]",
      "use_for": "Line charts, scatter plots, area charts",
      "pattern_code": "NUM_NUM"
    },
    {
      "id": "IT002",
      "name": "Range Dual Numeric",
      "signature": "[range, numeric, numeric]",
      "columns": 3,
      "example": "0-2: 30,45 | 2-4: 34,80 | 4-6: 38,60",
      "use_for": "Range-based comparisons, grouped data",
      "pattern_code": "RANGE_NUM_NUM"
    },
    {
      "id": "IT003",
      "name": "Three Column Numeric Series",
      "signature": "[numeric, numeric, numeric]",
      "columns": 3,
      "example": "0-2: 30, 45 | 2-4: 34, 80",
      "use_for": "Trivariate plotting, bubble charts",
      "pattern_code": "NUM_NUM_NUM"
    },
    {
      "id": "IT004",
      "name": "Single Value",
      "signature": "[numeric]",
      "columns": 1,
      "example": "60",
      "use_for": "KPI cards, single metric displays",
      "pattern_code": "SINGLE_NUM"
    },
    {
      "id": "IT005",
      "name": "Category Single Numeric",
      "signature": "[category, numeric]",
      "columns": 2,
      "example": "A: 60",
      "use_for": "Simple bar charts",
      "pattern_code": "CAT_NUM"
    },
    {
      "id": "IT006",
      "name": "Year Range Pivot",
      "signature": "[year, year, ...]",
      "columns": 3,
      "example": "2010: B,C | 2015: B,C",
      "use_for": "Time period comparison",
      "pattern_code": "YEAR_PIVOT"
    },
    {
      "id": "IT007",
      "name": "Category Percentage Simple",
      "signature": "[category, percentage]",
      "columns": 2,
      "example": "A: 32% | B: 40% | C: 28%",
      "use_for": "Pie charts, donut charts",
      "pattern_code": "CAT_PERCENT"
    },
    {
      "id": "IT008",
      "name": "Range Category Numeric",
      "signature": "[range, category, numeric]",
      "columns": 3,
      "example": "2-4: A,34 | 4-6: B,38",
      "use_for": "Range analysis with categories",
      "pattern_code": "RANGE_CAT_NUM"
    },
    {
      "id": "IT009",
      "name": "Event Time Mapping",
      "signature": "[event, datetime]",
      "columns": 2,
      "example": "Event A: 1-4-2015 | Event B: 10-4-2015 | Event C: 12-4-2015",
      "use_for": "Timeline charts, event tracking",
      "pattern_code": "EVENT_TIME"
    },
    {
      "id": "IT010",
      "name": "Location Value Mapping",
      "signature": "[location, numeric]",
      "columns": 2,
      "example": "Location A: 14 | Location B: 6 | Location C: 15",
      "use_for": "Geographic plots, maps",
      "pattern_code": "LOC_NUM"
    },
    {
      "id": "IT011",
      "name": "Demographic Split Female Male",
      "signature": "[age_group, female, male]",
      "columns": 3,
      "example": "10-20: 30,28 | 20-30: 34,22 | 30-40: 38,26",
      "use_for": "Population pyramids, demographic splits",
      "pattern_code": "DEMO_SPLIT"
    },
    {
      "id": "IT012",
      "name": "Three Dimensional XYZ",
      "signature": "[numeric, numeric, numeric]",
      "columns": 3,
      "example": "X: 1 | Y: 10 | Z: 30",
      "use_for": "3D scatter, bubble charts with size",
      "pattern_code": "XYZ_3D"
    },
    {
      "id": "IT013",
      "name": "Three Column with Index Variant",
      "signature": "[index, numeric, numeric]",
      "columns": 3,
      "example": "1: 10, - | 2: 34, 14 | 3: 38, 12",
      "use_for": "Indexed dual series",
      "pattern_code": "INDEX_NUM_NUM"
    },
    {
      "id": "IT014",
      "name": "Date Range Interval Start End",
      "signature": "[start_date, end_date]",
      "columns": 2,
      "example": "Start: 1-4-2015 | End: 6-4-2015",
      "use_for": "Gantt charts, interval visualization",
      "pattern_code": "DATE_INTERVAL"
    },
    {
      "id": "IT015",
      "name": "Four Column with Year Labels",
      "signature": "[label, year, year, ...]",
      "columns": 4,
      "example": "Y1, Y2, X | 2010: C,C,- | 2005: C,A,A",
      "use_for": "Time-series comparison",
      "pattern_code": "LABEL_YEAR_MULTI"
    },
    {
      "id": "IT016",
      "name": "Percentage Composition Two Part",
      "signature": "[category, percent, percent]",
      "columns": 3,
      "example": "A: 30%, 28% | B: 34%, 32% | C: 26%, 24%",
      "use_for": "Stacked bar charts, composition analysis",
      "pattern_code": "COMP_TWO_PART"
    },
    {
      "id": "IT017",
      "name": "OHLC Financial Open High Low Close",
      "signature": "[day, lower, close, open, upper]",
      "columns": 5,
      "example": "day 1: $10,$20,$60,$70 | day 2: $25,$30,$45,$65",
      "use_for": "Candlestick charts, financial data",
      "pattern_code": "OHLC"
    },
    {
      "id": "IT018",
      "name": "Day Time Series Multiple Periods",
      "signature": "[day, period1, period2, period3, period4]",
      "columns": 5,
      "example": "day 1: $10,$20,$60,$70 | day 2: $25,$30,$45,$65",
      "use_for": "Multi-period time series",
      "pattern_code": "DAY_MULTI_PERIOD"
    },
    {
      "id": "IT019",
      "name": "Single Column Value Only",
      "signature": "[numeric]",
      "columns": 1,
      "example": "Y: 510",
      "use_for": "Single metric KPI display",
      "pattern_code": "SINGLE_COL"
    },
    {
      "id": "IT020",
      "name": "Category Percentage Triple",
      "signature": "[category, percent, percent, percent]",
      "columns": 4,
      "example": "X: 10%, 48%, 42% | Y: 42%, 38%, 20% | Z: 24%, 36%, 40%",
      "use_for": "Three-part composition analysis",
      "pattern_code": "CAT_PERCENT_3"
    },
    {
      "id": "IT021",
      "name": "Numeric Matrix 3x3",
      "signature": "[category, numeric, numeric, numeric]",
      "columns": 4,
      "example": "D: 12,34,12 | E: 0,26,34 | F: 24,36,40",
      "use_for": "Heatmaps, matrix visualization",
      "pattern_code": "MATRIX_3X3"
    },
    {
      "id": "IT022",
      "name": "Size Allocation with Percentages",
      "signature": "[item, size, numeric, percent_a, percent_b]",
      "columns": 5,
      "example": "Pie 1: 2,100,65%,35% | Pie 2: 4,200,50%,50% | Pie 3: 6,400,80%,20%",
      "use_for": "Hierarchical pie/treemap with splits",
      "pattern_code": "SIZE_ALLOC_PERCENT"
    },
    {
      "id": "IT023",
      "name": "Percentage Parts Simple Two Col",
      "signature": "[category, part_a, part_b]",
      "columns": 3,
      "example": "A: 65%, 35% | B: 50%, 50% | C: 80%, 20%",
      "use_for": "Binary composition, stacked bar",
      "pattern_code": "COMP_BINARY"
    },
    {
      "id": "IT024",
      "name": "Ordered Categorical Four Level",
      "signature": "[order, level_1, level_2, level_3]",
      "columns": 4,
      "example": "1: Fruit, Citrus, Orange | 2: Fruit, Citrus, Lemon | 3: Meat, Pork, Chop",
      "use_for": "Sunburst, treemap, hierarchical charts",
      "pattern_code": "ORDERED_CAT_4LVL"
    },
    {
      "id": "IT025",
      "name": "Numeric Value Simple",
      "signature": "[numeric]",
      "columns": 1,
      "example": "-50 or 230",
      "use_for": "Gauge, number display",
      "pattern_code": "NUM_VAL"
    },
    {
      "id": "IT026",
      "name": "Category Numeric Simple Two Col",
      "signature": "[category, numeric]",
      "columns": 2,
      "example": "A: 14 | B: 16 | C: 12",
      "use_for": "Simple bar, column chart",
      "pattern_code": "CAT_NUM_SIMPLE"
    },
    {
      "id": "IT027",
      "name": "Three Column with Index Row",
      "signature": "[index, numeric, numeric, numeric]",
      "columns": 4,
      "example": "1: 30, 10, - | 2: 34, 14, (empty) | 3: 38, 12, (empty)",
      "use_for": "Indexed multi-series",
      "pattern_code": "INDEX_NUM_3COL"
    },
    {
      "id": "IT028",
      "name": "Logical Matrix Row Col Binary",
      "signature": "[row_cat, col_cat_A, col_cat_B, col_cat_C]",
      "columns": 4,
      "example": "Row: A, ¬A | Col: B, W, X, ¬B, Y, Z",
      "use_for": "Confusion matrix, logical heatmap",
      "pattern_code": "LOGIC_MATRIX"
    },
    {
      "id": "IT029",
      "name": "Category Index Numeric Dual",
      "signature": "[category, numeric, numeric]",
      "columns": 3,
      "example": "A: 30, 14 | B: 34, 16 | C: 38, 10",
      "use_for": "Grouped bar, multi-metric comparison",
      "pattern_code": "CAT_DUAL_NUM"
    },
    {
      "id": "IT030",
      "name": "Roman Numeral Index",
      "signature": "[roman_index, numeric]",
      "columns": 2,
      "example": "I: 14 | II: 6",
      "use_for": "Indexed value display",
      "pattern_code": "ROMAN_INDEX"
    },
    {
      "id": "IT031",
      "name": "Category with Four Numeric Values",
      "signature": "[category, numeric, numeric, numeric, numeric]",
      "columns": 5,
      "example": "A: 14, 6, 10 | B: 16, 12, 8",
      "use_for": "Multi-metric comparison",
      "pattern_code": "CAT_4NUM"
    },
    {
      "id": "IT032",
      "name": "Mixed Letter Label Header",
      "signature": "[label, numeric, numeric, numeric]",
      "columns": 4,
      "example": "Y1, Y2, X headers with grid values",
      "use_for": "Labeled multi-series",
      "pattern_code": "LABEL_HEADER"
    },
    {
      "id": "IT033",
      "name": "Category Time Period Matrix",
      "signature": "[category, time_period, time_period, time_period]",
      "columns": 4,
      "example": "A: [2000:C], [2005:C], [2010:-]",
      "use_for": "Cross-tabulation, period comparison",
      "pattern_code": "CAT_TIME_PERIOD"
    },
    {
      "id": "IT034",
      "name": "Two Numeric Column Paired",
      "signature": "[numeric, numeric]",
      "columns": 2,
      "example": "30, 28 | 34, 22 | 38, 26",
      "use_for": "Paired series comparison",
      "pattern_code": "NUM_PAIRED"
    },
    {
      "id": "IT035",
      "name": "Percentage Pair with Category",
      "signature": "[category, percent, percent]",
      "columns": 3,
      "example": "X: 30%, 28% | Y: 34%, 32% | Z: 26%, 24%",
      "use_for": "Dual percentage comparison",
      "pattern_code": "CAT_PERCENT_PAIR"
    },
    {
      "id": "IT036",
      "name": "Date Start End Formatted",
      "signature": "[start_datetime, end_datetime]",
      "columns": 2,
      "example": "1-4-2015 to 6-4-2015 | 10-4-2015 to 18-4-2015 | 12-4-2015 to 20-4-2015",
      "use_for": "Timeline, Gantt chart",
      "pattern_code": "DATE_START_END"
    },
    {
      "id": "IT037",
      "name": "Hierarchy Level 1-2-3-4",
      "signature": "[order, level_1, level_2, level_3]",
      "columns": 4,
      "example": "1: Fruit, Citrus, Orange | 2: Fruit, Citrus, Lemon | 3: Meat, Pork, Chop",
      "use_for": "Sunburst, treemap, icicle chart",
      "pattern_code": "HIERARCHY_4LVL"
    },
    {
      "id": "IT038",
      "name": "X Y with Expression",
      "signature": "[numeric, expression]",
      "columns": 2,
      "example": "Y: 30, 14 Y1+Y2 | Y: 34, 16 Y1+Y2",
      "use_for": "Derived series, calculated columns",
      "pattern_code": "NUM_EXPR"
    },
    {
      "id": "IT039",
      "name": "Category Numeric Expression",
      "signature": "[category, numeric, expression]",
      "columns": 3,
      "example": "A: 30, 14 Y1+Y2",
      "use_for": "Category with derived metric",
      "pattern_code": "CAT_NUM_EXPR"
    },
    {
      "id": "IT040",
      "name": "Numeric Range Boundary",
      "signature": "[numeric_min, numeric_max]",
      "columns": 2,
      "example": "-20 to +50 (as Start/End labels)",
      "use_for": "Range indicators, bounds visualization",
      "pattern_code": "NUM_RANGE_BOUND"
    }
  ]
}
```

---

## SUMMARY

- **Total Distinct Input Types Identified:** 40
- **Unique Column Counts:** 1, 2, 3, 4, 5 columns
- **Most Common Pattern:** Category + numeric (appears ~8 variants)
- **Most Complex:** OHLC Financial (5 columns with semantic structure)
- **Simplest:** Single numeric value (1 column)

All input types now mapped with:
- Unique ID (IT001-IT040)
- Name
- Signature notation
- Example data
- Suggested chart types
- Pattern code (for programmatic use)

Ready for HTML-to-Markdown conversion reference.
