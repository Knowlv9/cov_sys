

// Prefecture Select tag

const get_options = (group) => {
	console.log("set_options");
	let li = [];
	for (var v in group) {
		li.push([group[v]["size"], v]);
	}
	li.sort((a, b) => {return b[0] - a[0];});	// descending order
	li = li.map(v => {return v[1]; });
	return li;
}

const set_options = (select, options) => {
	for (var p of options) {
		if (p == "NaN") { continue; }
		// const new_option = document.createElement("option");
		// new_option.innerHTML = p;
		// select.appendChild(new_option);
	}
	return ;
}

const create_th = (p, value) => {
	const th = document.createElement("th");
	th.innerHTML = p;
	th.setAttribute("scope", "row")
	return th;
}

const create_td = (dic, key) => {
	const td = document.createElement("td");
	td.innerHTML = (key != "") ? dic[key] : "";

	if (key == "size" || key == "") {
		td.classList.add("text-center");
	}

	if (key != ""){
		return td;
	}

	if (dic["email"] != null){
		td.classList.add("text-success");

		const span = document.createElement("span");
		span.classList.add("safe");
		td.appendChild(span);
	}else{
		td.classList.add("text-danger");

		const span = document.createElement("span");
		span.classList.add("unsafe");
		td.appendChild(span);
	}
	return td;
}


const set_table = (tbody, group, prf) => {
	for (var p of prf) {
		if (p == "NaN") { continue; }
		const tr = document.createElement("tr");

		const th_prf = create_th(p, group[p]);
		const td_filename = create_td(group[p], "filename");
		const td_size = create_td(group[p], "size");
		const td_result = create_td(group[p], "");

		tr.appendChild(th_prf);
		tr.appendChild(td_filename);
		tr.appendChild(td_size);
		tr.appendChild(td_result);
		tbody.appendChild(tr);
	}
	return ;
}

const HomeClass = class {
	constructor(g) {
		this.group = group;
		this.select = document.getElementById("PrfSelect");
		this.tbody = document.getElementById("GroupTbody");
		this.datelist = datelist;
		this.options = get_options(this.group);
	}

	get get_group(){
		return this.group;
	}

	setElement(){
		console.log("setElement");
		setSelect(this.select, this.datelist);
		set_table(this.tbody, this.group, this.options);
	}
}


var home = new HomeClass();
home.setElement();
