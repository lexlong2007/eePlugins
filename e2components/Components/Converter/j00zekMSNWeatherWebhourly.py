try:
    from Components.Converter.MSNWeatherWebhourly import MSNWeatherWebhourly as j00zekMSNWeatherWebhourly
except Exception:
    try:
        from Components.Converter.FhromaMSNWeatherWebhourly import FhromaMSNWeatherWebhourly as j00zekMSNWeatherWebhourly
    except Exception:
        from Components.Converter.j00zekMissingConverter import j00zekMissingConverter as j00zekMSNWeatherWebhourly
