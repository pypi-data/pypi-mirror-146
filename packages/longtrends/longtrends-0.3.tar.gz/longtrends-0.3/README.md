# longtrends

A package to download long-term Google Trends.

## Introduction

[Google Trends](https://trends.google.com/trends), downloadable by API using [pytrends](https://pypi.org/project/pytrends/), limits the time period which can be downloaded using a single request. Each request is scaled between 0 and 100, making comparison between different time periods difficult. This package automatically downloads overlapping trends and rescales them, providing trend data across a long-term period.

## Installation

`pip install longtrends`

## Requirements

Requires [pytrends](https://pypi.org/project/pytrends/), installed automatically with `pip`.

## Usage

```
from longtrends import rescale_overlaps, trends_plot, get_overlapping_trends
from datetime import datetime

# Get overlapping trends
olympics = get_overlapping_trends(
                                keyword='olympics',
                                start_date=datetime(2021, 7, 4),
                                end_date=datetime(2021, 8, 29),
                                days_delta=10)

# Plot overlapping trends
trends_plot(olympics)

# Rescale overlaps
olympics_rescaled = rescale_overlaps(olympics)

# Plot rescaled trends
trends_plot(olympics_rescaled)
```

## Disclaimer

This is not an official or supported product. It is provided without warranty under MIT license.
