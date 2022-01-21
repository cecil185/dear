# Import libraries
from functions import set_title

# Custom imports
from functions.multipage import MultiPage
from pages import health_check, upload_data, visualize_data

set_title.set()

# Create an instance of the app
app = MultiPage()

# Add applications to navigation pane
app.add_page("Upload Data", upload_data.app)
app.add_page("Health Check", health_check.app)
app.add_page("Visualize Data", visualize_data.app)

# Triggers run for everything
app.run()
