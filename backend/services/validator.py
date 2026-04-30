def normalize_signals(signals):
    return {
        "qa": signals.get("qa") if isinstance(signals.get("qa"), dict) else None,
        "hiring": signals.get("hiring") if isinstance(signals.get("hiring"), dict) else None,
        "saas": signals.get("saas") if isinstance(signals.get("saas"), dict) else None,
        "tech": signals.get("tech") if isinstance(signals.get("tech"), dict) else None,
        "negative": signals.get("negative") if isinstance(signals.get("negative"), dict) else None,
        "website_health": signals.get("website_health") if isinstance(signals.get("website_health"), int) else None,
    }