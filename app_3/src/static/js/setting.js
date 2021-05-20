
const url = "./getFileparams";

function getFileparams(){
	fetch(url, {
		method: "GET",
		mode: "cors",
	})
	.then(result => {
		return result.json();
	})
	.then(data => {
		const labels = data["output"]["params"].map((val) => {
			return val.trim();
		});

		for (var el of document.getElementsByName("outputId")) {
			const val = el.value.trim();
			if (labels.indexOf(val) > -1) { el.checked = true; }
		}
	})
	.catch(error => {
		console.log(error);
	})
}

const postMasterfilePath = (li) => {
	let formData = new FormData();

	formData.append("outputColList", li);

	const url = './settingMasterfile';
	data = {
		method: "POST",
		mode: 'cors',
		body: formData
	}
	fetch(url, data)
	.then(response => response.json())
	.then(result => {
		console.log("success", result);
	})
	.catch(error => {
		console.log("error", error);
	})
}

const masterbtn = document.getElementById('saveConf');

const getOutPutCols = () => {
	const els = document.getElementsByName("outputId");
	let li = [];

	for (var el of els) {
		if (el.checked) {
			li.push(el.value)
		}
	}
	return JSON.stringify(li);
}

getFileparams();
masterbtn.addEventListener('click', () => {
	const li = getOutPutCols();
	postMasterfilePath(li);
});
