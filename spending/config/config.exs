# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.
use Mix.Config

# General application configuration
config :spending,
  ecto_repos: [Spending.Repo]

# Configures the endpoint
config :spending, Spending.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "8QFRLJW8A6nBCp8a+QnXqXoa+ZIUkgzfViD/dZcYm+WpPhu2pOiyHAK4kE4ehP7B",
  render_errors: [view: Spending.ErrorView, accepts: ~w(html json)],
  pubsub: [name: Spending.PubSub,
           adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env}.exs"
