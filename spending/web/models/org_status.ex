defmodule Spending.OrganisationStatus do
  use Spending.Web, :model

  schema "organisationstatus" do
    field :department, :string
    field :year, :integer
    field :month, :integer
    field :present, :boolean
  end

  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:department])
    |> validate_required([:department])
  end
end
