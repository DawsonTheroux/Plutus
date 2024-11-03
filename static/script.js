function select_config() {
  const selected_file = document.getElementById('config-select').value;
  const modify_button = document.getElementById('modify-button')
  const use_config_button = document.getElementById('use-config-button')

  const contentElement = document.getElementById('content');

  // document.getElementById('file-content').style.display = 'none';
  if(selected_file) {
    const content = document.getElementById('file-' + selected_file).textContent;
    console.log("FILE:" + selected_file);
    /* Enable the config display view */
    contentElement.textContent = content;
    document.getElementById('file-content').style.display = 'block';

    /* Enable the buttons */
    modify_button.href = `/modify?config=${encodeURIComponent(selected_file)}`;
    modify_button.querySelector('button').disabled = false;
    // modify_button.disabled = false;

    use_config_button.href = `/importStatement?config=${encodeURIComponent(selected_file)}`;
    use_config_button.querySelector('button').disabled = false;
    // use_config_button.disabled = false;
  }else {
    console.log("NO FILE");
    contentElement.textContent = "";
    document.getElementById('file-content').style.display = 'none';
    modify_button.href = '#';
    modify_button.querySelector('button').disabled = true;
    use_config_button.href = '#';
    use_config_button.querySelector('button').disabled = true;
  }
}

function create_new_config() {
  const regex = /^[a-zA-Z0-9-_]+$/;
  let invalid_config = true;
  while(invalid_config){
    const config_name = prompt("Please name the new configuration:", "new_config");
    if(regex.test(config_name)){
      window.location.href = `/modify?config=${encodeURIComponent(config_name)}`;
      invalid_config = false;
      return;
    }else{
      alert("Invalid config name. Valid characters include letters, numbers, underscore, and dash.");
    }
  }
}

function refresh_list(transaction_type) {
  const config = JSON.parse(document.getElementById("config-div").innerText);
  const list_div = document.getElementById(transaction_type + "-div");

  // Delete the existing UL if it exists.
  child_ul = list_div.firstChild;
  if(child_ul){
    list_div.removeChild(child_ul);
  }

  const new_ul = document.createElement("ul");
  config[transaction_type]["categories"].forEach((item, index) => {
    const new_li = document.createElement('li');
    const new_label = document.createElement('label');
    new_label.setAttribute('for', `item${index}`);
    new_label.textContent = item;

    const new_button = document.createElement('button');
    new_button.setAttribute('id', `item${index}`);
    new_button.textContent = "X";
    new_button.setAttribute('onclick', "remove_category('" + transaction_type + "', '" + item + "'); refresh_list('" + transaction_type + "')");

    new_li.appendChild(new_label);
    new_li.appendChild(new_button);
    new_ul.appendChild(new_li);
  });
  list_div.appendChild(new_ul);
}

function add_category(transaction_type) {
  const regex = /^[a-zA-Z0-9-_]+$/;
  category_input = document.getElementById(transaction_type + "-input")
  config_div = document.getElementById("config-div");
  current_config = JSON.parse(config_div.innerText);

  /* Do not allow duplicates in the categories */
  if(current_config[transaction_type]["categories"].includes(category_input.value)){
    alert("You cannot add duplicate categories!");
  /* Only allow the regex values */
  }else if(!regex.test(category_input.value)){
    alert("Invalid config name. Valid characters include letters, numbers, underscore, and dash.");
  }else{
    current_config[transaction_type]["categories"].push(category_input.value);
  }
  category_input.value= "";
  config_div.innerText = JSON.stringify(current_config);
}

function remove_category(transaction_type, category) {
  config_div = document.getElementById("config-div");
  current_config = JSON.parse(config_div.innerText);
  if(current_config[transaction_type]["categories"].includes(category)){
    current_config[transaction_type]["categories"] = current_config[transaction_type]["categories"].filter(item => item !== category);
  }
  config_div.innerText = JSON.stringify(current_config);
}

function finish_config(config_name) {
  const current_config = JSON.parse(document.getElementById("config-div").innerText);
  fetch(`/modify?config=${config_name}`, {
    method: "POST",
    headers: {
      "Content-Type":"application/json"
    },
    body: JSON.stringify(current_config)
  })
  .then(response => {
    if(response.ok) {
      window.location.href = `/upload?config=${encodeURIComponent(config_name)}`;
    }else{
      alert("There was a problem updating the config");
    }
  })
  // Push the config.
  // Redirect to the file upload.
}
