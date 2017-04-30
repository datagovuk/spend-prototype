
defmodule Spending.SpendRecord do
  use Spending.Web, :model

  schema "spendrecord" do
    field :department, :string
    field :entity, :string
    field :date, :date
    field :expense_type, :string
    field :expense_area, :string
    field :supplier, :string
    field :transaction, :string
    field :amount, :decimal
    field :description, :string
    field :supplier_postcode, :string
    field :supplier_type, :string
    field :contract_number, :string
    field :project_code, :string
    field :expenditure_type, :string
  end

  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:department])
    |> validate_required([:department])
  end
end
