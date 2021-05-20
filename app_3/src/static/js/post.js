
const clear_row = (tbody) => {
	const els = document.getElementsByClassName("data-row");

	if (els.length === 0) { return ; }

	while (els.length > 0) {
		tbody.firstChild.remove();
	}
	
	return ;
}

const create_td = (val) => {
	const td = document.createElement("td");
	if (typeof(val) == "object" && val != null) {
		td.appendChild(val);
	}else {
		td.innerHTML = val;
	}
	return td;
}

const create_td_check = (prf) => {
	const checkbox = document.createElement("input");
	checkbox.id = `check_${prf}`;
	checkbox.setAttribute("type", "checkbox");
	checkbox.setAttribute("value", prf);
	checkbox.classList.add("form-check-input");
	return create_td(checkbox);
}

const create_td_filename = (dic, prf, data) => {
	let value = "";
	if (data.indexOf(dic["filename"]) > -1) {
		value = dic["filename"];
	}

	return create_td(value);
}

const check = (p, email) => {
	const el = document.getElementById(`check_${p}`);
	const flag = ((p == null || email == null) || email.length === 0) ? false : true;
	el.checked = flag;

	return ;
}

const create_td_temp = (prf) => {
	const select = document.createElement("select");
	const option = document.createElement("option");

	option.setAttribute("value", "default");
	option.innerHTML = "default";

	select.appendChild(option);

	return create_td(select);
}

const create_td_btn = (prf) => {
	const button = document.createElement("button");
	button.classList.add("btn");
	button.setAttribute("value", `post_${prf}`);
	button.innerHTML = "送信";

	const td = document.createElement("td");
	td.appendChild(button);
	return td;
}

const show_list = (data) => {
	const tbody = document.getElementById("PostListTbody");

	clear_row(tbody);

	for (var prf in group){
		const tr = document.createElement("tr");
		tr.classList.add("data-row");
		const sub_email = (group[prf]["email"] == null) ? "" :
			`${group[prf]["email"].substring(0, 5)}...`;

		const td_check = create_td_check(prf);
		const td_prf = create_td(prf);
		const td_file = create_td_filename(group[prf], prf, data);
		const td_email = create_td(sub_email);
		const td_temp = create_td_temp(prf);
		const td_btn = create_td_btn(prf);


		tr.appendChild(td_check);
		tr.appendChild(td_prf);
		tr.appendChild(td_file);
		tr.appendChild(td_email);
		tr.appendChild(td_temp);
		tr.appendChild(td_btn);

		tbody.appendChild(tr);
		check(prf, group[prf]["email"]);
	}
}

const showDatelist = (date) => {
	let formData = new FormData();
	if (date.value == ""){ return ;}
	formData.append("date", date.value);

	fetch("./show_list", {
		method: "POST",
		mode: "cors",
		body: formData
	})
	.then(result => result.json())
	.then(data =>{
		show_list(data["list"]);
	});
}

const sendEmail = () => {
	console.log("send email");
}

const PostClass = class {
	constructor(){
		this.datelist = datelist;
		this.select = document.getElementById("DateOptions");
	}

	setElement(){
		setSelect(this.select, this.datelist);
	}
	setEvent(){
	}
}


const post = new PostClass();
post.setElement();
post.setEvent();
