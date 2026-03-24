from fastapi import FastAPI

from tracker.router import content, ui

app = FastAPI(
    title="MailTracker",
    description="Simple dashboard for creating email tracking pixels and reviewing opens.",
)
app.include_router(ui.router)
app.include_router(content.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
