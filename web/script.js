document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("predictForm");
    const resultsDiv = document.getElementById("results");
    const errorDiv = document.getElementById("error");

    if (!form) {
        console.error("Form element with ID 'predictForm' not found!");
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        resultsDiv.innerHTML = "";
        errorDiv.innerHTML = "";

        const inputValues = [
            parseFloat(document.getElementById("day1").value),
            parseFloat(document.getElementById("day2").value),
            parseFloat(document.getElementById("day3").value),
            parseFloat(document.getElementById("day4").value),
            parseFloat(document.getElementById("day5").value)
        ];

        try {
            const response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ last_values: inputValues })
            });

            console.log("Response status:", response.status);
            if (!response.ok) {
                const errorData = await response.json();
                console.error("Error from server:", errorData);
                errorDiv.innerText = errorData.error || "An error occurred!";
                return;
            }

            const data = await response.json();
            console.log("Success:", data);

            resultsDiv.innerHTML = `
                <h3>Predicted Prices:</h3>
                <ul>
                    ${data.predicted_prices.map(price => `<li>${price.toFixed(2)}</li>`).join("")}
                </ul>
                <canvas id="predictionChart"></canvas>
            `;

            const ctx = document.getElementById("predictionChart").getContext("2d");
            const chartData = [...inputValues, ...data.predicted_prices];
            const labels = [
                "Day 1",
                "Day 2",
                "Day 3",
                "Day 4",
                "Day 5",
                "Prediction 1",
                "Prediction 2",
                "Prediction 3",
                "Prediction 4",
                "Prediction 5"
            ];

            if (window.predictionChart && typeof window.predictionChart.destroy === "function") {
                window.predictionChart.destroy();
            }

            window.predictionChart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Stock Prices and Predictions",
                        data: chartData,
                        borderColor: "rgba(0, 255, 255, 1)",
                        backgroundColor: "rgba(0, 255, 255, 0.2)",
                        borderWidth: 2,
                        pointRadius: 6,
                        pointBackgroundColor: "rgba(255, 99, 132, 1)",
                        pointHoverRadius: 8,
                    }]
                },
                options: {
                    responsive: true,
                    animation: {
                        duration: 1000,
                        easing: "easeOutQuart"
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return `Price: ₹${context.raw.toFixed(2)}`;
                                }
                            },
                            backgroundColor: "rgba(0, 0, 0, 0.7)",
                            titleColor: "#fff",
                            bodyColor: "#fff",
                            borderColor: "rgba(255, 255, 255, 0.5)",
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                color: "white"
                            },
                            grid: {
                                color: "rgba(255, 255, 255, 0.1)"
                            }
                        },
                        y: {
                            ticks: {
                                color: "white"
                            },
                            grid: {
                                color: "rgba(255, 255, 255, 0.1)"
                            }
                        }
                    }
                }

            });

        } catch (err) {
            console.error("Unexpected error:", err);
            errorDiv.innerText = "An unexpected error occurred!";
        }
    });
});