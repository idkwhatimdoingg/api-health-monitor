const API_URL = "http://127.0.0.1:8000";


// ----------------------------
// Load API Status
// ----------------------------

async function loadStatus() {

    console.log("LOAD STATUS START", new Date());

    try {

        const response = await fetch(
            `${API_URL}/api/status`
        );

        const data = await response.json();

        await displayAPIs(data);


    } catch (error) {

        console.error(
            "Failed to load API status:",
            error
        );

    }

    console.log("LOAD STATUS END", new Date());
}



// ----------------------------
// Get Uptime
// ----------------------------

async function getUptime(apiName) {

    try {

        const response = await fetch(
            `${API_URL}/api/uptime/${encodeURIComponent(apiName)}`
        );


        const data = await response.json();


        return data.uptime;


    } catch(error) {

        console.error(
            "Failed to get uptime:",
            error
        );


        return "N/A";

    }

}



// ----------------------------
// Display API Cards
// ----------------------------

async function displayAPIs(apis) {

    const container = document.getElementById(
        "api-container"
    );


    for (const api of apis) {


        let statusClass = "warning";


        if (api.status.includes("Operational")) {

            statusClass = "healthy";

        }

        else if (api.status.includes("Down")) {

            statusClass = "danger";

        }



        const uptime = await getUptime(
            api.name
        );



        const cardID = api.name.replace(
            /[^a-zA-Z0-9]/g,
            "-"
        );



        let card = document.getElementById(
            `card-${cardID}`
        );



        // Create card once

        if (!card) {


            card = document.createElement(
                "div"
            );


            card.className = "api-card";


            card.id = `card-${cardID}`;


            container.appendChild(card);

        }



        // Update existing card

        card.innerHTML = `

       <h2>
    ${api.name}

    <span class="api-id">
        #${api.id}
    </span>
</h2>


            <p class="${statusClass}">
                ${api.status}
            </p>


            <p>
                HTTP:
                ${api.status_code}
            </p>


            <p>
                Latency:
                ${api.latency} ms
            </p>


            <p>
                Uptime:
                ${uptime}
            </p>


            <p>
                Checked:
                ${api.checked_at}
            </p>

        `;

    }

}



// ----------------------------
// Add API
// ----------------------------

async function addAPI() {

    const name = document.getElementById(
        "api-name"
    ).value.trim();



    const url = document.getElementById(
        "api-url"
    ).value.trim();



    if (!name || !url) {

        alert(
            "Please enter both name and URL"
        );

        return;

    }



    try {


        const response = await fetch(
            `${API_URL}/api/endpoints`,
            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },


                body: JSON.stringify({

                    name: name,

                    url: url

                })

            }

        );



        if (!response.ok) {

            throw new Error(
                "Failed to add API"
            );

        }



        document.getElementById(
            "api-name"
        ).value = "";



        document.getElementById(
            "api-url"
        ).value = "";




        // Immediately check APIs

        await fetch(
            `${API_URL}/api/monitor/run`,
            {
                method: "POST"
            }
        );



        // Refresh cards

        await loadStatus();



        alert(
            "API added successfully"
        );



    } catch(error) {


        console.error(
            "Failed to add API:",
            error
        );


        alert(
            "Failed to add API"
        );

    }

}
// ----------------------------
// Remove API
// ----------------------------

async function removeAPI() {

    const id = document
        .getElementById("api-id")
        .value
        .trim();


    if (!id) {

        alert("Please enter API ID");

        return;

    }


    try {

        const response = await fetch(
            `${API_URL}/api/endpoints/${id}`,
            {
                method: "DELETE"
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to remove API"
            );

        }


        document.getElementById(
            "api-id"
        ).value = "";


        await loadStatus();


        alert(
            "API removed successfully"
        );


    } catch(error) {


        console.error(
            "Remove API error:",
            error
        );


        alert(
            "Failed to remove API"
        );

    }

}


// ----------------------------
// Start Dashboard
// ----------------------------

loadStatus();


// Refresh every 60 seconds

setInterval(
    loadStatus,
    60000
);
console.log("APP JS LOADED");