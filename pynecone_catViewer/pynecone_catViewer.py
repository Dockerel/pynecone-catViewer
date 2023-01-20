"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc
import requests

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(pc.State):
    image_url = "https://avatars.githubusercontent.com/u/74302278?v=4"
    fetching = False

    def start_fetching(self):
        self.fetching = True

    def fetch_cat(self):
        response = requests.get("https://aws.random.cat/meow")
        json = response.json()
        self.image_url = json.get("file")
        self.fetching = False


def index():
    return pc.center(
        pc.vstack(
            pc.heading(
                "Cat Viewer",
                size="3xl",
                marginTop="1em",
            ),
            pc.button("Give me a cat!", on_click=[State.start_fetching, State.fetch_cat]),
            pc.cond(
                State.fetching,
                pc.circular_progress(
                    is_indeterminate=True,
                ),
            ),
            pc.cond(
                State.image_url != "" and State.fetching == False,
                pc.image(
                    src=State.image_url,
                    height="25em",
                    width="25em",
                ),
            ),
            spacing="3em",
        ),
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
