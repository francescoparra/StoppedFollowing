# StoppedFollowing

StoppedFollowing is a Python app designed to help you identify individuals who have unfollowed you on Instagram.

## Prerequisites

- Python (>= 3.11)
- Poetry (>= 1.7.0)

## How to Run

1. Clone the project:
    ```bash
    git clone https://github.com/francescoparra/StoppedFollowing.git
    cd project_folder
    ```

2. Install dependencies:
    ```bash
    poetry install
    ```

3. Copy `.env.sample` to `.env` and insert your Instagram credentials.

4. Run the project in your console:
    ```bash
    poetry run python app.py
    ```

## How the App Works

The first time you run the app, it creates and populates `previous_time_followers.json` with your current followers. Subsequent runs compare your current followers with the saved data, creating and then updating `unfollowed_you.json` with unfollower information in descending order by date.

## License

This project is licensed under the [MIT License](LICENSE).
