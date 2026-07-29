const API_URL = "http://127.0.0.1:8000/api/status";


async function loadDashboard() {

    const response = await fetch(API_URL);

    const data = await response.json();


    const dashboard = document.getElementById("dashboard");

    dashboard.innerHTML = "";


    for (const api of data) {


        const uptimeResponse = await fetch(
            `http://127.0.0.1:8000/api/uptime/${encodeURIComponent(api.name)}`
        );


        const uptimeData = await uptimeResponse.json();



        let statusClass = "";


        if (api.status.includes("Operational")) {

            statusClass = "operational";

        } 
        
        else if (api.status.includes("issue")) {

            statusClass = "warning";

        } 
        
        else {

            statusClass = "down";

        }



        dashboard.innerHTML += `

        <div class="card">

            <h2>${api.name}</h2>


            <h3 class="${statusClass}">
                ${api.status}
            </h3>


            <p>
                HTTP: ${api.status_code}
            </p>


            <p>
                Latency:
                ${api.latency} ms
            </p>


            <p>
                Uptime:
                ${uptimeData.uptime}
            </p>


            <p>
                Checks:
                ${uptimeData.total_checks}
            </p>


            <p>
                Last checked:
                ${api.checked_at}
            </p>

        </div>

        `;

    }

}


loadDashboard();


setInterval(
    loadDashboard,
    30000
);