import importlib


def test_web_server_cors_defaults_to_local_origins_without_credentials(monkeypatch):
    monkeypatch.delenv("CORS_ALLOW_ORIGINS", raising=False)

    app_module = importlib.import_module("web_server.app")

    cors_middleware = next(
        middleware
        for middleware in app_module.app.user_middleware
        if middleware.cls.__name__ == "CORSMiddleware"
    )

    assert cors_middleware.kwargs["allow_origins"] == [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]
    assert cors_middleware.kwargs["allow_credentials"] is False
