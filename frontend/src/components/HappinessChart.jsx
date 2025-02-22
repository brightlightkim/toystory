import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

const HappinessChart = () => {
  const [happinessData, setHappinessData] = useState([]);
  const [labels, setLabels] = useState([]);

  // useEffect(() => {
  //   const fetchHappinessScore = async () => {
  //     try {
  //       const response = await fetch("http://localhost:8000/emotion/happiness_score/");
  //       const data = await response.json();

  //       setHappinessData((prevData) => [...prevData.slice(-9), data.happiness_score]);
  //       setLabels((prevLabels) => [...prevLabels.slice(-9), new Date().toLocaleTimeString()]);
  //     } catch (error) {
  //       console.error("Error fetching happiness score:", error);
  //     }
  //   };

  //   const interval = setInterval(fetchHappinessScore, 5000);
  //   return () => clearInterval(interval);
  // }, []);

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Happiness Score",
        data: happinessData,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.2,
      },
    ],
  };

  return (
    <div className="w-full max-w-lg mx-auto p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-center text-lg font-semibold mb-4">Real-time Happiness Score</h2>
      <Line data={chartData} />
    </div>
  );
};

export default HappinessChart;