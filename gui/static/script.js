// 页面加载时调用“/show”接口
window.onload = async function() {
    try {
        const response = await fetch('/show');
        const data = await response.json(); // 获取 JSON 数据

        // 检查返回的 code 是否为2000，确保请求成功
        if (data.code === 2000) {
            const deviceList = document.getElementById('deviceList');
            const devices = data.devices; // 设备列表

            // 遍历设备列表，生成复选框和设备ID
            devices.forEach(device => {
                const item = document.createElement('div');
                item.classList.add('device-item');
                item.innerHTML = `
                    <input type="checkbox" id="${device}" name="${device}">
                    <label for="${device}">${device}</label>
                `;
                deviceList.appendChild(item);
            });

            // 全选按钮功能
            const selectAllBtn = document.getElementById('selectAll');
            selectAllBtn.onclick = () => {
                const checkboxes = document.querySelectorAll('.device-item input[type="checkbox"]');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = true;
                });
            };

            // 提交按钮功能
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.onclick = async () => {
                const selectedDevices = [];
                const checkboxes = document.querySelectorAll('.device-item input[type="checkbox"]:checked');
                checkboxes.forEach(checkbox => {
                    selectedDevices.push(checkbox.id);
                });

                // 发送选中的设备ID到“/selectedDevice”接口
                if (selectedDevices.length > 0) {
                    const response = await fetch('/selectedDevice', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ devices: selectedDevices })
                    });

                    const result = await response.json();
                    console.log(result); // 输出接口返回的结果
                } else {
                    alert("请先选择设备！");
                }
            };

        } else {
            console.error('接口返回错误码:', data.code);
        }
    } catch (error) {
        console.error('Error fetching device data:', error);
    }
};
