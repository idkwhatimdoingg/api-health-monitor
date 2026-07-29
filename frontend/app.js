const API_URL = "http://127.0.0.1:8000/api/status";


async function loadDashboard() {

    try {

        const response = await fetch(API_URL);

        const data = await response.json();


        const dashboard = document.getElementById("dashboard");

        dashboard.innerHTML = "";


        data.forEach(api => {


            let statusClass = "";


            if (api.status.includes("Operational")) {

                statusClass = "operational";

            } else if (api.status.includes("issue")) {

                statusClass = "warning";

            } else {

                statusClass = "down";

            }



            dashboard.innerHTML += `

            <div class="card">

                <h2>${api.name}</h2>

                <h3 class="${statusClass}">
                    ${api.status}
                </h3>

                <p>
                    HTTP Status: ${api.status_code}
                </p>

                <p>
                    Latency: ${api.latency} ms
                </p>

                <p>
                    Last Checked: ${api.checked_at}
                </p>

            </div>

            `;

        });


    } catch (error) {

        document.getElementById("dashboard").innerHTML =
        `
        <div class="card">
            Failed to connect to API backend.
        </div>
        `;

        console.error(error);

    }

}


loadDashboard();