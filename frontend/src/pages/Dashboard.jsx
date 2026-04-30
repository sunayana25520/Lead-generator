import { useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");

  // FETCH AFTER UPLOAD
  const fetchData = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/get-sheet");
      const rows = res?.data || [];
      setData(
        rows.map((row, index) => ({
          ...row,
          rowNumber: index + 2,
        }))
      );
    } catch (err) {
      console.error("Fetch error:", err);
      setData([]);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Select CSV");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      await axios.post("http://127.0.0.1:8000/analyze", formData);
      await fetchData();
    } catch (err) {
      console.error("Upload error:", err);
      alert("Backend not reachable");
    } finally {
      setLoading(false);
    }
  };

  // ✅ FINAL FIXED FUNCTION (WORKS 100%)
  const updateCell = async (i, key, value, sheetRow, col) => {
    const updated = [...data];
    const targetIndex = updated.findIndex((item) => item.rowNumber === sheetRow);

    const indexToUpdate = targetIndex >= 0 ? targetIndex : i;

    updated[indexToUpdate] = {
      ...updated[indexToUpdate],
      [key]: value,
    };

    setData(updated);

    try {
      await axios.post("http://127.0.0.1:8000/update-cell", {
        row: sheetRow,
        col,
        value,
      });
    } catch (err) {
      console.error(err);
    }
  };

  // CARDS
  const total = data.length;
  const contacted = data.filter(
    (d) => d["Status"] === "Sent" || d["Status"] === "Replied"
  ).length;

  // DOWNLOAD CSV
  const downloadCSV = () => {
    if (!data.length) return;

    const headers = Object.keys(data[0]).filter((h) => h !== "rowNumber");

    const rows = data.map((row) =>
      headers.map((h) => `"${row[h] ?? ""}"`).join(",")
    );

    const csv = [headers.join(","), ...rows].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "google_sheet_data.csv";
    a.click();
  };

  // FILTER + SORT
  const filtered = data
    .filter((d) =>
      d["Company Name"]
        ?.toLowerCase()
        .includes(search.toLowerCase())
    )
    .sort((a, b) => b["Lead Score"] - a["Lead Score"]);

  // SCORE COLORS
  const getScoreClass = (score) => {
    if (score >= 7) return "score high";
    if (score >= 4) return "score mid";
    return "score low";
  };

  return (
    <div className="app">

      <div className="nav">Lead Generator</div>

      <div className="container">

        <h1>Lead Dashboard</h1>

        {/* TOP BAR */}
        <div className="top-bar">
          <div className="left">
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <button onClick={handleUpload}>
              {loading ? "Analyzing..." : "Start Analysis"}
            </button>
          </div>

          <div className="right">
            <button className="download" onClick={downloadCSV}>
              Download CSV
            </button>
          </div>
        </div>

        {/* CARDS */}
        <div className="cards">
          <div className="card">
            <p>Total Leads</p>
            <h2>{total}</h2>
          </div>

          <div className="card">
            <p>Contacted</p>
            <h2>{contacted}</h2>
          </div>
        </div>

        {/* SEARCH */}
        <input
          className="search"
          placeholder="Search company..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {/* TABLE */}
        <div className="table-box">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Company</th>
                <th>Website</th>
                <th>Tech</th>
                <th>Hiring</th>
                <th>QA</th>
                <th>Product</th>
                <th>Pain Point</th>
                <th>Message</th>
                <th>Score</th>
                <th>Status</th>
                <th>Follow-up</th>
                <th>Notes</th>
              </tr>
            </thead>

            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="13">Analyzing...</td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td colSpan="13">Upload CSV to view data</td>
                </tr>
              ) : (
                filtered.map((row, i) => (
                  <tr key={row.rowNumber || i}>
                    <td>{i + 1}</td>
                    <td>{row["Company Name"]}</td>
                    <td>{row["Website"]}</td>
                    <td>{row["Tech Stack"]}</td>
                    <td>{row["Hiring Detected (Y/N)"]}</td>
                    <td>{row["QA Signals (Y/N)"]}</td>
                    <td>{row["Product Type"]}</td>
                    <td>{row["Pain Point"]}</td>
                    <td>{row["Personalization Line"]}</td>

                    <td>
                      <span className={getScoreClass(row["Lead Score"])}>
                        {row["Lead Score"]}
                      </span>
                    </td>

                    {/* STATUS */}
                    <td>
                      <select
                        value={row["Status"] || "Not Contacted"}
                        onChange={(e) =>
                          updateCell(
                            i,
                            "Status",
                            e.target.value,
                            row.rowNumber,
                            10
                          )
                        }
                      >
                        <option>Not Contacted</option>
                        <option>Sent</option>
                        <option>Replied</option>
                      </select>
                    </td>

                    {/* FOLLOW-UP */}
                    <td>
                      <input
                        type="date"
                        value={row["Follow-up Date"] || ""}
                        onChange={(e) =>
                          updateCell(
                            i,
                            "Follow-up Date",
                            e.target.value,
                            row.rowNumber,
                            11
                          )
                        }
                      />
                    </td>

                    {/* ✅ NOTES (WORKING NOW) */}
                    <td>
                      <textarea
                        rows={2}
                        value={row["Notes"] || ""}
                        onChange={(e) =>
                          updateCell(
                            i,
                            "Notes",
                            e.target.value,
                            row.rowNumber,
                            12
                          )
                        }
                      />
                    </td>

                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
}