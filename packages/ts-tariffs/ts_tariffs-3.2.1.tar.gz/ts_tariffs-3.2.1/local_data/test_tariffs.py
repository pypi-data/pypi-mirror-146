tariff_data = {
  "charges": [
    {
      "name": "retail_tou",
      "charge_type": "TouTariff",
      "consumption_unit": "kWh",
      "rate_unit": "dollars / kWh",
      "adjustment_factor": 1.005,
      "tou": {
        "time_bins": [
          7,
          21,
          24
        ],
        "bin_rates": [
          0.06,
          0.10,
          0.06
        ],
        "bin_labels": [
          "off-peak",
          "peak",
          "off-peak"
        ]
      },
    },
    {
      "name": "lrecs",
      "charge_type": "SingleRateTariff",
      "rate": 0.007,
      "consumption_unit": "kWh",
      "rate_unit": "dollars / kWh",
      "adjustment_factor": 1.005
},
    {
      "name": "srecs",
      "charge_type": "SingleRateTariff",
      "rate": 0.0114,
      "consumption_unit": "kWh",
      "rate_unit": "dollars / kWh",
      "adjustment_factor": 1.005
},
    {
      "name": "connection_tariff",
      "charge_type": "ConnectionTariff",
      "rate": 315.0,
      "consumption_unit": "day",
      "frequency_applied": "day",
      "rate_unit": "dollars / day",
      "adjustment_factor": 1.0
    },
    {
      "name": "tuos_energy",
      "charge_type": "SingleRateTariff",
      "rate": 0.011,
      "consumption_unit": "kWh",
      "rate_unit": "dollars / kWh",
      "adjustment_factor": 1.005

},
    {
      "name": "ICC11B_energy",
      "charge_type": "SingleRateTariff",
      "rate": 0.0021,
      "consumption_unit": "kWh",
      "rate_unit": "dollars / kWh",
      "adjustment_factor": 1.0
    },
    {
      "name": "ICC11B_demand",
      "charge_type": "DemandTariff",
      "consumption_unit": "kVA",
      "rate": 0.850,
      "frequency_applied": "month",
      "rate_unit": "dollars / kVA / month",
      "adjustment_factor": 1.0
    },
    {
      "name": "ICC11B_location",
      "charge_type": "DemandTariff",
      "consumption_unit": "kW",
      "rate": 1.190,
      "frequency_applied": "month",
      "rate_unit": "dollars / kW / month",
      "adjustment_factor": 1.0
    },
    {
      "name": "duos_capacity",
      "charge_type": "CapacityTariff",
      "consumption_unit": "kVA",
      "capacity": 10000.0,
      "rate": 0.400,
      "frequency_applied": "month",
      "rate_unit": "dollars / kVA / month",
      "adjustment_factor": 1.0
    },
    {
      "name": "aemo_market_energy_fee",
      "charge_type": "SingleRateTariff",
      "rate": 0.00055,
      "consumption_unit": "kWh",
      "rate_unit": "dollars / kWh",
      "adjustment_factor": 1.005
    },
    {
      "name": "aemo_market_daily_fee",
      "charge_type": "ConnectionTariff",
      "rate": 0.003700,
      "consumption_unit": "day",
      "frequency_applied": "day",
      "rate_unit": "dollars / day",
      "adjustment_factor": 1.0
    },
    {
      "name": "aemo_market_ancillary_fee",
      "charge_type": "SingleRateTariff",
      "rate": 0.00121,
      "consumption_unit": "kWh",
      "rate_unit": "dollars / kWh",
      "adjustment_factor": 1.005
    },
    {
      "name": "metering_charge",
      "charge_type": "ConnectionTariff",
      "rate": 100.0,
      "consumption_unit": "month",
      "frequency_applied": "month",
      "rate_unit": "dollars / month",
      "adjustment_factor": 1.0
    },
  ]
}
