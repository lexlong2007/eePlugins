try:
    from Components.Converter.MSNWeatherWebCurrent import MSNWeatherWebCurrent as j00zekMSNWeatherWebCurrent
except Exception:
    try:
        from Components.Converter.FhromaMSNWeatherWebCurrent import FhromaMSNWeatherWebCurrent as j00zekMSNWeatherWebCurrent
    except Exception:
        from Components.Converter.j00zekMissingConverter import j00zekMissingConverter as j00zekMSNWeatherWebCurrent
