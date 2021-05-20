const setSelect = (select, li) => {
	console.log(li);
	for (var d of li) {
		const date = new Date(d[1]);
		let delta = new Date() - date;
		delta = parseInt(delta / (1000*60*60*24)); // day
		if (delta > 31) { break; }

		const op = document.createElement("option");
		op.setAttribute("value", d[0])
		op.innerHTML = d[1];
		select.appendChild(op);
	}
	return ;
}
