import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

const HappinessChart = () => {
  const [happinessData, setHappinessData] = useState([]);
  const [labels, setLabels] = useState([]);

  useEffect(() => {
    const fetchHappinessScore = async () => {
      try {
        const response = await fetch("http://localhost:8000/emotion/happiness_score/");
        const data = await response.json();

        setHappinessData((prevData) => [...prevData.slice(-9), data.happiness_score]);
        setLabels((prevLabels) => [...prevLabels.slice(-9), new Date().toLocaleTimeString()]);
      } catch (error) {
        console.error("Error fetching happiness score:", error);
      }
    };

    const interval = setInterval(fetchHappinessScore, 5000);
    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Happiness Index",
        data: happinessData,
        fill: true,
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: (context) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, context.chart.height);
          gradient.addColorStop(0, "rgba(75, 192, 192, 0.5)"); // Light Green for Happy
          gradient.addColorStop(0.5, "rgba(255, 255, 255, 0)"); // Neutral
          gradient.addColorStop(1, "rgba(255, 99, 132, 0.5)"); // Light Red for Sad
          return gradient;
        },
        tension: 0.3,
        pointRadius: 4,
        pointBackgroundColor: happinessData.map(value =>
          value >= 1 ? "😊" :
          value >= 0 ? "🙂" :
          value > -1 ? "😐" :
          value > -2 ? "😞" : "😢"
        ),
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top",
      },
      tooltip: {
        callbacks: {
          label: (context) => `Happiness: ${context.raw.toFixed(2)}`,
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Time",
          font: { size: 14 },
        },
      },
      y: {
        title: {
          display: true,
          text: "Happiness Index",
          font: { size: 14 },
        },
        suggestedMin: -2,
        suggestedMax: 2,
        grid: {
          color: (context) =>
            context.tick.value === 0 ? "black" : "rgba(200, 200, 200, 0.5)", // Dark line at 0
        },
        ticks: {
          callback: (value, index, values) => {
            if (index === 0) return "Sad 😢"; // Bottom-most tick
            if (index === values.length - 1) return "Happy 😊"; // Top-most tick
            if (value >= 1) return "☺️"; // Variation of Happy emoji
            if (value > 0) return "🙂";
            if (value == 0) return "😐";  // Neutral Happy emoji
            if (value > -1) return "😕"; // Neutral Sad emoji
            if (value > -2) return "😞"; // Variation of Sad emoji
            return "😢"; // Sad emoji
          },
        },
      },
    },
    animation: {
      duration: 1000,
      easing: "easeInOutQuart",
    },
  };

  return (
    <div className="w-full max-w-lg mx-auto p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-center text-lg font-semibold mb-4">Real-time Happiness Score</h2>
      <div className="relative h-80">
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
};

export default HappinessChart;