defmodule Spending.PageController do
  use Spending.Web, :controller

  alias Spending.Repo
  alias Spending.{SpendRecord, OrganisationStatus}

  import Ecto.Query, only: [from: 2]

  def get_departments() do
    [
     "Cabinet Office",
     "Communities and Local Government",
     "Department For Transport",
     "Department for Business, Energy and Industrial Strategy",
     "Department for Business, Innovation and Skills",
     "Department for Culture Media and Sport",
     "Department for Education",
     "Department for International Development",
     "Department for Transport",
     "Department for Work and Pensions",
     "Department of Health",
     "Export Credits Guarantee Department",
     "Government Actuary's Department",
     "HM Land Registry",
     "HM Procurator General and Treasury Solicitor",
     "HM Revenue and Customs",
     "HM Treasury",
     "Home Office",
     "Ministry of Defence",
     "Ministry of Justice",
     "Office of the Advocate General for Scotland",
     "Ofqual",
     "Scotland Office",
     "UK Trade and Investment",
    ]
  end

  def supplier_query(:nil, q), do: q
  def supplier_query("", q), do: q
  def supplier_query(supplier, q) do
    from s in q,
    where: ilike(s.supplier, ^("#{supplier}%"))
  end

  def dept_query(:nil, q), do: q
  def dept_query("", q), do: q
  def dept_query(dept, q) do
    from s in q,
    where: ilike(s.department, ^dept)
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

  def status_key(r) do
    "#{r.department}-#{to_string(r.year)}-#{to_string(r.month)}"
  end

  def status(conn, %{}=params) do


    records = Repo.all(OrganisationStatus)
    |> Enum.reduce(%{}, fn r, acc ->
      Map.put(acc, status_key(r), r.present)
    end)

    render conn, "status.html", departments: get_departments(), records: records
  end
end
