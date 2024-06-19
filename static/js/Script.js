let addresses_information = { addresses_number: 0, info: new Object() };
let repository_information = { objects_number: 0, info: new Object() };
let trucks = { trucks_number: 0, info: new Object() };
const csrftoken = document.cookie.split("=")[1];
console.log(csrftoken);
let addresses_ids = ["center"];

function generateSections() {
  const numSections = document.getElementById("numSectionsInput").value;
  const sectionsContainer = document.getElementById("sectionsContainer");

  if (sectionsContainer) {
    sectionsContainer.innerHTML = "";
    addresses_ids = ["center"];
    // Generate addresses ids
    for (i = 0; i < numSections; i++) {
      let ad_id = `ad${i + 1}`;
      addresses_ids.push(ad_id);
    }
  }

  // Generate sections
  for (let i = 0; i < addresses_ids.length; i++) {
    const section = document.createElement("div");
    section.className = "section";
    if (i == 0) {
      section.id = "center";
    } else {
      section.id = `ad${i}`;
    }
    section.style.marginTop = `${i > 1 ? "10px" : "0"}`; // add margin top for each section

    // Generate section title
    const title = document.createElement("h2");
    if (i == 0) {
      title.textContent = `مركز الأنطلاق`;
    } else {
      title.textContent = `العنوان ${i}`;
    }
    section.appendChild(title);

    // Generate ID field
    const idField = document.createElement("div");
    idField.className = "field";
    idField.classList.add("id_title");
    idField.innerHTML = `
      <label for="id${i}">ID:</label>
      <span>${addresses_ids[i]}</span>
    `;
    section.appendChild(idField);

    // Generate name field
    const nameField = document.createElement("div");
    nameField.className = "field";
    nameField.innerHTML = `
      <label for="name${i}">الأسم:</label>
      <input type="text" id="name_${addresses_ids[i]}" placeholder="إذا لم يتم ادخال اسم سيتم اعتماد المعرف كاسم">
      <h4>يرجى إدخال الزمن بين العنوان والعناوين الأخرى:</h4>
    `;
    section.appendChild(nameField);

    // Generate time field

    for (let d = 0; d < addresses_ids.length; d++) {
      let current_id = addresses_ids[d];

      if (section.id != current_id) {
        const timeField = document.createElement("div");
        timeField.className = "field";
        let tt;
        if (current_id == "center") {
          tt = "center";
        } else {
          tt = `العنوان ${d}`;
        }
        timeField.innerHTML = `
            <label for="time${d}">${tt}</label>
            <input type="number" id="${section.id}_time_${current_id}" min="0">
        `;
        section.appendChild(timeField);
      }
    }

    sectionsContainer.appendChild(section);
  }
}

// Fill addresses object
function get_addresses_info() {
  const addresses_ob = document.getElementById("sectionsContainer");
  const elements_id = addresses_ob.children;
  for (let i = 0; i < elements_id.length; i++) {
    ad_id = elements_id[i].id;
    ad_name = document.getElementById(`name_${addresses_ids[i]}`);
    ad_time_to = new Object();
    for (let d = 0; d < addresses_ids.length; d++) {
      if (ad_id != addresses_ids[d]) {
        let ele = document.getElementById(`${ad_id}_time_${addresses_ids[d]}`);
        ad_time_to[addresses_ids[d]] = ele.value;
      }
    }
    addresses_information["addresses_number"] = addresses_ids.length;
    addresses_information["info"][ad_id] = {
      id: ad_id,
      name: ad_name.value,
      time_to: ad_time_to,
    };
  }
}

// Boxes
let boxes_id = [];
function generateTable() {
  get_addresses_info();
  const numBoxes = document.getElementById("numBoxes").value;
  for (let i = 1; i <= numBoxes; i++) {
    s = `box_${i}`;
    boxes_id.push(s);
  }

  const tableBody = document
    .getElementById("boxesTable")
    .getElementsByTagName("tbody")[0];

  tableBody.innerHTML = ""; // Clear previous rows

  for (let i = 1; i <= numBoxes; i++) {
    const row = tableBody.insertRow();
    row.insertCell().innerHTML = `${i}`;
    row.insertCell().innerHTML = `<input type="number" min=1 id='w_box_${i}' placeholder="وزن الصندوق">`;
    row.insertCell().innerHTML = `<input type="number" min=1 id='v_box_${i}' placeholder="قيمة الصندوق">`;
    const select_b = document.createElement("select");
    select_b.id = `de_box_${i}`;
    for (let k = 1; k < addresses_ids.length; k++) {
      const f_ch = document.createElement("option");
      f_ch.value = addresses_ids[k];
      f_ch.innerText = addresses_ids[k];
      select_b.appendChild(f_ch);
    }

    row.insertCell().appendChild(select_b);
    row.insertCell().innerHTML = `<input type="text" id='n_box_${i}' placeholder="الأسم" oninput="updateName(this)">`;
  }
}

function get_boxes_information() {
  repository_information["objects_number"] = boxes_id.length;
  for (let i = 1; i <= boxes_id.length; i++) {
    box_name = document.getElementById(`n_box_${i}`).value;
    box_weight = document.getElementById(`w_box_${i}`).value;
    box_value = document.getElementById(`v_box_${i}`).value;
    box_going_to = document.getElementById(`de_box_${i}`).value;
    repository_information["info"][boxes_id[i - 1]] = {
      id: boxes_id[i - 1],
      name: box_name,
      weight: box_weight,
      value: box_value,
      going_to: box_going_to,
    };
  }
}

function updateName(input) {
  if (input.value === "") {
    input.value = "إذا لم يتم ادخال اسم سيتم اعتماد المعرف كاسم";
  }
}
// trucks
let trucks_id = [];
function generateTableTR() {
  const truckCount = parseInt(document.getElementById("truckCount").value);
  const tableBody = document
    .getElementById("truckTable")
    .getElementsByTagName("tbody")[0];
  tableBody.innerHTML = ""; // Clear existing rows

  for (let k = 1; k <= truckCount; k++) {
    trucks_id.push(`tr_${k}`);
  }

  for (let i = 1; i <= truckCount; i++) {
    const row = tableBody.insertRow();
    const idCell = row.insertCell();
    const capacityCell = row.insertCell();
    const nameCell = row.insertCell();

    idCell.innerHTML = `${i}`;

    const capacityInput = document.createElement("input");
    capacityInput.type = "number";
    capacityInput.min = "1";
    capacityInput.id = `c_${trucks_id[i - 1]}`;
    capacityCell.appendChild(capacityInput);

    const nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.placeholder = "إذا لم يتم ادخال اسم سيتم اعتماد المعرف كاسم";
    nameInput.id = `n_${trucks_id[i - 1]}`;
    nameCell.appendChild(nameInput);
  }
}

function get_trucks_information() {
  trucks["trucks_number"] = trucks_id.length;
  for (let i = 1; i <= trucks_id.length; i++) {
    tr_name = document.getElementById(`n_tr_${i}`).value;
    tr_capacity = document.getElementById(`c_tr_${i}`).value;
    trucks["info"][trucks_id[i - 1]] = {
      id: trucks_id[i - 1],
      name: tr_name,
      capacity: tr_capacity,
    };
  }
}

function submitInfo() {
  get_boxes_information();
  get_trucks_information();
  const ch = document.getElementById("checking");

  let boxes_check = false;
  for (let i = 0; i < boxes_id.length; i++) {
    if (
      repository_information["info"][`${boxes_id[i]}`]["value"] == "" ||
      repository_information["info"][`${boxes_id[i]}`]["weight"] == "" ||
      repository_information["info"][`${boxes_id[i]}`]["value"] == "0" ||
      repository_information["info"][`${boxes_id[i]}`]["weight"] == "0"
    ) {
      boxes_check = true;
    }
  }

  let truck_check = false;
  for (let i = 0; i < trucks_id; i++) {
    if (
      trucks["info"][trucks_id[i]]["capacity"] == "" ||
      trucks["info"][trucks_id[i]]["capacity"] == "0"
    ) {
      truck_check = true;
    }
  }

  let msg = "";
  if (
    addresses_ids.length <= 1 ||
    boxes_id.length < 1 ||
    trucks_id.length < 1
  ) {
    msg += "لم تدخل معلومات كافية";
  } else if (boxes_check) {
    msg += " | ";
    msg += "راجع معلومات الصناديق";
  } else if (truck_check) {
    msg += " | ";
    msg += "راجع معلومات الشاحنات";
  } else {
    call_back_end();
  }
  if (msg != "") {
    ch.innerText = msg;
  }
}

// show_result(data);

function extract_remaining_goods(re_goods) {
  const tableBody = document
    .getElementById("remainning_goods")
    .getElementsByTagName("tbody")[0];

  tableBody.innerHTML = ""; // Clear previous rows
  i = 0;
  for (e in re_goods) {
    i++;
    const row = tableBody.insertRow();
    row.insertCell().innerHTML = `${i}`;
    row.insertCell().innerHTML = e;
    row.insertCell().innerHTML = re_goods[e]["box_weight"];
    row.insertCell().innerHTML = re_goods[e]["box_value"];
    row.insertCell().innerHTML = re_goods[e]["box_destination"];
    row.insertCell().innerHTML = re_goods[e]["box_name"];
  }
}

function extract_not_used_trucks(re_trucks) {
  const tableBody = document
    .getElementById("trucks_out")
    .getElementsByTagName("tbody")[0];

  tableBody.innerHTML = ""; // Clear previous rows
  i = 0;
  for (e in re_trucks) {
    i++;
    const row = tableBody.insertRow();
    row.insertCell().innerHTML = `${i}`;
    row.insertCell().innerHTML = e;
    row.insertCell().innerHTML = re_trucks[e]["truck_capacity"];
    row.insertCell().innerHTML = re_trucks[e]["truck_name"];
  }
}

function extract_dist(trucks) {
  let con = document.getElementById("destcon");
  con.innerHTML = "";
  for (e in trucks) {
    let boxes = trucks[e]["truck_boxes"];
    bx = "<br>";
    for (b in boxes) {
      bx += boxes[b];
      bx += "<br>";
    }

    let ads = trucks[e]["truck_addresses"];
    ax = "<br>";
    for (b in ads) {
      ax += ads[b];
      ax += "<br>";
    }

    let txt = `
    <div class="con-dist-tr">
          <h4>معلومات الشاحنة</h4>
          <span>ID</span><span>${e}</span><br />
          <span>الأسم</span><span>${trucks[e]["truck_name"]}</span><br />
          <span>السعة</span><span>${trucks[e]["truck_capacity"]}</span><br />
          <h4>معلومات الحمولة</h4>
          <span>وزن الحمولة</span><span>${trucks[e]["truck_load_weight"]}</span><br />
          <span>قيمة الحمولة</span><span>${trucks[e]["truck_load_value"]}</span><br />
          <span>الصناديق ضمن الشاحنة</span>
          <span>
          ${bx}
          </span>
          
          <h4>معلومات المسار</h4>
          <span>الزمن الكلي للمسار</span> <span>${trucks[e]["Route_Total_time"]}</span><br />
          
          <span>العناوين ضمن المسار</span>
          <span>${ax}</span>
          <span>المسار</span><br />
          <span>${trucks[e]["truck_route"]}</span>
        </div>
  
    `;
    con.innerHTML += txt;
  }
}

// Call Backend
function call_back_end() {
  let sending = {
    details: {
      addresses_information: addresses_information,
      repository_information: repository_information,
      trucks: trucks,
    },
  };
  fetch(`/api/get_result/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(sending),
  })
    .then((response) => response.json())
    .then((data) => {
      show_result(data);
      console.log(data);
    })
    .catch((error) => {
      console.log(error);
    });
}

function show_result(data) {
  extract_remaining_goods(data["remaining_goods"]);
  extract_not_used_trucks(data["trucks_out"]);
  extract_dist(data["trucks"]);
}
