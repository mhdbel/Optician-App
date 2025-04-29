// Dashboard.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Dashboard = () => {
  // Filter states
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [category, setCategory] = useState('');
  // Data state
  const [salesData, setSalesData] = useState({
    dates: [],
    total_sales: [],
    invoice_counts: []
  });

  const fetchSalesData = async () => {
    const formattedStart = startDate.toISOString().slice(0, 10);
    const formattedEnd = endDate.toISOString().slice(0, 10);
    try {
      const response = await axios.get('/api/reports/historical-sales', {
        params: {
          start_date: formattedStart,
          end_date: formattedEnd,
          category: category  // send empty string if not selected
        }
      });
      setSalesData(response.data);
    } catch (error) {
      console.error('Error fetching historical sales data:', error);
    }
  };

  // Update data when filters change
  useEffect(() => {
    fetchSalesData();
  }, [startDate, endDate, category]);

  // Chart configuration
  const chartData = {
    labels: salesData.dates,
    datasets: [
      {
        label: 'Total Sales',
        data: salesData.total_sales,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        fill: false,
        tension: 0.1,
      },
      {
        label: 'Invoice Count',
        data: salesData.invoice_counts,
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        fill: false,
        tension: 0.1,
      }
    ]
  };

  return (
    <div className="container mt-4">
      <h1>Enhanced Optician Store Dashboard</h1>
      <div className="row my-4">
        {/* Date Range Filters */}
        <div className="col-md-4">
          <label>Start Date</label>
          <DatePicker
            selected={startDate}
            onChange={(date) => setStartDate(date)}
            dateFormat="yyyy-MM-dd"
            className="form-control"
          />
        </div>
        <div className="col-md-4">
          <label>End Date</label>
          <DatePicker
            selected={endDate}
            onChange={(date) => setEndDate(date)}
            dateFormat="yyyy-MM-dd"
            className="form-control"
          />
        </div>
        {/* Product Category Filter */}
        <div className="col-md-4">
          <label>Product Category</label>
          <select
            className="form-select"
            value={category}
            onChange={e => setCategory(e.target.value)}
          >
            <option value="">All</option>
            <option value="frames">Frames</option>
            <option value="lenses">Lenses</option>
            <option value="accessories">Accessories</option>
          </select>
        </div>
      </div>
      {/* Chart */}
      <div className="card p-3">
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Dashboard;
