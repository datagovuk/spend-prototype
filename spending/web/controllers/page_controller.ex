defmodule Spending.PageController do
  use Spending.Web, :controller

  alias Spending.Repo
  alias Spending.SpendRecord

  import Ecto.Query, only: [from: 2]

  def get_departments() do
    [
      "Cabinet Office",
      "Communities & Local Government",
      "Department of Business, Innovation and Skills",
      "Department for Business, Innovation and Skills",
      "Department for Culture Media and Sport",
      "Department for Education",
      "DEPARTMENT FOR TRANSPORT",
      "Department for Transport",
      "Department For Transport",
      "Department for Work and Pensions",
      "DFID",
      "HM Procurator General and Treasury Solicitor",
    ]
  end

  def supplier_query(:nil, q), do: q
  def supplier_query("", q), do: q
  def supplier_query(supplier, q) do
    from s in q,
    where: ilike(s.supplier, ^("#{supplier}%"))
  end

  def index(conn, %{}=params) do
    page =
      from s in SpendRecord,
      order_by: :id

    department = Map.get(params, "department")
    if department do
      page = from s in page,
        where: s.department == ^department
    end

    page =
    Map.get(params, "supplier")
    |> supplier_query(page)

    page = Repo.paginate(page, params)

    render conn, "index.html",
      departments: get_departments(),
      records: page.entries,
      page_number: page.page_number,
      page_size: page.page_size,
      total_pages: page.total_pages,
      total_entries: page.total_entries,
      department: Map.get(params, "department"),
      supplier: Map.get(params, "supplier")
  end
end
