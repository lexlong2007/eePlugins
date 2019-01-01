try:
    from Components.Converter.MSNWeatherWebhourly import MSNWeatherWebhourly as BlackHarmonyMSNWeatherWebhourly
except Exception:
    from Components.Converter.j00zekMissingConverter import j00zekMissingConverter as BlackHarmonyMSNWeatherWebhourly
