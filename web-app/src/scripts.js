document.addEventListener('DOMContentLoaded', function() {
    try {
      let app = firebase.app();
      let features = ['auth', 'database', 'messaging', 'storage'].filter(feature => typeof app[feature] === 'function');
    } catch (e) {
      console.error(e);
    }

    let play_status
    let air_status
    let today = new Date();
    let hour = today.getHours()
    if (hour < 10) {
      hour = '0' + hour
    }
    let time = hour + ":" + today.getMinutes()
    let feeding_status

    var getData = firebase.database().ref();
    setInterval(() => { getData.on('value', function(snapshot) {
        let data = snapshot.val()
        let temp = data['TEMP']
        let feeding_time = data['FEEDING_TIME']
        air_status = data['AIR']
        play_status = data['PLAYING']
        feeding_status = data['FEEDING']
        console.log(temp, air_status, feeding_status)
        document.getElementById("temp").innerHTML = temp
        document.getElementById("timepicker").value = feeding_time
        if (temp > 28 && air_status == 0) {
          document.getElementById("temperature").style.background = '#f4ccccff'
          document.getElementById("temp-status").innerHTML = 'ร้อน 🥵'
          document.getElementById("temperature").classList.add("shake");
        } else {
          document.getElementById("temperature").style.background = '#d9ead3ff'
          document.getElementById("temp-status").innerHTML = 'ปกติ 😊'
          document.getElementById("temperature").classList.remove("shake");
        }

        if (time === feeding_time) {
          Feeding()
        }
        document.getElementById("air").checked = air_status
        if (play_status == 0)
          document.getElementById("play").classList.remove("disabled");
        if (feeding_status == 0) {
          document.getElementById("feed").classList.remove("disable");
          document.getElementById("feed").innerHTML = 'เติมอาหารตอนนี้ 🍖'
        }
      });
    }, 2000);

    document.getElementById("feed").addEventListener("click", Feeding);
    function Feeding() {
      let newData = {
        FEEDING: 1,
      };

      document.getElementById("feed").classList.add("disable");
      document.getElementById("feed").innerHTML = 'กำลังเติมอาหาร'
      return firebase.database().ref().update(newData);
    }

    document.getElementById("timepicker").addEventListener("change", SetFeedingTime);
    function SetFeedingTime() {
      let newData = {
        FEEDING_TIME: document.getElementById("timepicker").value,
      };

      return firebase.database().ref().update(newData);
    }

    document.getElementById("air").addEventListener("click", ToggleAir);
    function ToggleAir() {
      if (air_status == 1) {
        air_status = 0
      } else {
        air_status = 1
      }
      let newData = {
        AIR: air_status,
      };
    
      return firebase.database().ref().update(newData);
    }

    document.getElementById("play").addEventListener("click", TogglePlay);
    function TogglePlay() {
      document.getElementById("play").classList.add("disabled");

      let newData = {
        PLAYING: 1,
      };

      return firebase.database().ref().update(newData)
    }
  });