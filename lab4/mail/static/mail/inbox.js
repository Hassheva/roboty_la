document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {
    load_mailbox('inbox');
    console.log("work inbox end");
  });
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  //submit--
  document.querySelector('#compose-form').onsubmit = () => {
    const newrecipients = document.querySelector('#compose-recipients').value;
    console.log(newrecipients);
    const newsubject = document.querySelector('#compose-subject').value;
    console.log(newsubject);
    const newbody = document.querySelector('#compose-body').value;
    console.log(newbody);

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: newrecipients,
          subject: newsubject,
          body: newbody
      })
    })
    .then(response => response.json())
    .then(result => {
        // Вивести результат в консоль
        console.log(result);
        alert(result.message);
        document.querySelector('#compose-recipients').value = '';
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
        if (result.message != undefined){
          load_mailbox('sent');
        } else {
          compose_email();
          alert(result.error);
        }
        
    });
    //stop form from submitting
    return false;
  }
  //--reply
  document.querySelector('#detail-form').onsubmit = () => {
    console.log("reply click");
    const reply_id = document.querySelector('#detail_id').value;
    console.log(reply_id);
    ReplyonMail(reply_id);
    return false;
  }
  //
});
//----------------------------------------------------------------------------
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
//----------------------------------------------------------------------------
function load_mailbox(mailbox) {
  console.log(`work ${mailbox} start`);
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  console.log(`work fetch( /emails/${mailbox})`);
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Вивести листи в консоль
    console.log(`emails=${emails}`);
    console.log(emails);
    // ... зробити з листами щось інше ...
    emails.forEach(function(email) {
      console.log(`email=${email}`);
      console.log(email);
      CreateListMail(email);
  })
    
}).then( () => ZipUnzip());

}
//----------------------------------------------------------------------------
function CreateListMail(email) {
  console.log("start createlistmail");
  let maindiv = document.createElement('div');
      maindiv.classList.add("createmaindiv");
      maindiv.id = 'mail_' + email.id;
      //

  let checkboxelement = document.createElement('input');
      checkboxelement.type = "checkbox";
      checkboxelement.classList.add("checkindiv");
      checkboxelement.id = email.id;
      //

  let labelelement = document.createElement('label');
      //labelelement.innerHTML = "chek";
      labelelement.classList.add("labelclass");
      console.log("label start");
      console.log(labelelement);
      labelelement.htmlFor = email.id;
      //

  let blockjsondiv = document.createElement('div');
      blockjsondiv.classList.add("blockjson");
      blockjsondiv.addEventListener('click', function() {
        console.log(`Цей елемент натиснуто! ${email.id}`);
        jsonmail.classList.add("blockjsonmail");
        jsonmail.classList.remove("blockjsonmail_bold");
        blockjsondiv.classList.add("blockjson_background");
        //
        ViewDetailMail(email.id)
        MailStatusRead(email.id)
        //
        });
      //

  let jsonmail = document.createElement('div');
      jsonmail.classList.add("blockjsonmail");
      jsonmail.classList.add("blockjsonmail_bold");
      if (document.querySelector('h3').innerText == "Sent") {
        jsonmail.innerHTML = email.recipients;
        console.log(jsonmail);
      } else {
        jsonmail.innerHTML = email.sender;
        console.log(jsonmail);
      }
      //

  let jsonsubject = document.createElement('div');
      jsonsubject.classList.add("blockjsonsubject");
      jsonsubject.innerHTML = email.subject;
      console.log(jsonsubject);
      //

  let jsontimestamp = document.createElement('div');
      jsontimestamp.classList.add("blockjsontimestamp");
      jsontimestamp.innerHTML = email.timestamp;
      console.log(jsontimestamp);
      blockjsondiv.append(jsontimestamp);
      //

  if (email.read) {
    jsonmail.classList.add("blockjsonmail");
    blockjsondiv.classList.add("blockjson_background");
    jsonmail.classList.remove("blockjsonmail_bold");
  } else {
    jsonmail.classList.add("blockjsonmail");
    jsonmail.classList.add("blockjsonmail_bold");
  }
  //

      document.querySelector('#emails-view').append(maindiv);
      maindiv.append(checkboxelement);
      maindiv.append(labelelement);
      maindiv.append(blockjsondiv);
      blockjsondiv.append(jsonmail);
      blockjsondiv.append(jsonsubject);
      blockjsondiv.append(jsontimestamp);

}
//----------------------------------------------------------------------------
function MailStatusRead(id_email) {
  fetch(`/emails/${id_email}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}
//----------------------------------------------------------------------------
function ViewDetailMail(id_email) {
  console.log(`detail for ${id_email} mail start`);
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'block';
  //
  fetch(`/emails/${id_email}`)
  .then(response => response.json())
  .then(email => {
    // Вивести лист до консолі
    console.log(email);
    // ... зробити з листом щось інше ...
    document.getElementById('detail_id').value = id_email;
    document.getElementById('detail_sender').innerHTML = email.sender;
    document.getElementById('detail_recipients').innerHTML = email.recipients;
    document.getElementById('detail_subject').innerHTML = email.subject;
    document.getElementById('detail_timestamp').innerHTML = email.timestamp;
    document.getElementById('detail_body').innerHTML = email.body;
});

}
//----------------------------------------------------------------------------
function ReplyonMail(id_email) {
  console.log(`reply for ${id_email} mail start`);
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#detail-view').style.display = 'none';
  //
  fetch(`/emails/${id_email}`)
  .then(response => response.json())
  .then(email => {
    // Вивести лист до консолі
    console.log(email);
    // ... зробити з листом щось інше ...
    console.log(`repley to ${email.sender}`);
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.includes("Re:")) {
      document.querySelector('#compose-subject').value = `${email.subject}`;  
    } else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `<< On ${email.timestamp} ${email.sender} write: ${email.body} >>\n`;
    //
});
}
//----------------------------------------------------------------------------
function ZipUnzip() {
  console.log(`zip unzip mail start`);
  if (document.querySelector('h3').innerText == 'Inbox') {
    let zip = document.createElement('button');
        zip.className = "btn btn-primary";
        zip.id = 'zipbtn';
        zip.innerText = 'ZIP';
        document.querySelector('#emails-view').append(zip);
        console.log("add zip")
        //
        zip.onclick = () => {
          let zipcheck = document.getElementsByClassName('checkindiv');
          console.log(zipcheck);
          [...zipcheck].forEach(element => {
            if (element.checked){
              console.log(element.id);
              document.getElementById('mail_' + element.id).remove()
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: true
                })
              })
             }
          })
        }
        //
  }
  if (document.querySelector('h3').innerText == 'Archive') {
    let unzip = document.createElement('button');
        unzip.className = "btn btn-primary";
        unzip.id = 'unzipbtn';
        unzip.innerText = 'unZIP';
        document.querySelector('#emails-view').append(unzip);
        console.log("add unzip")
        //
        unzip.onclick = () => {
          let unzipcheck = document.getElementsByClassName('checkindiv');
          console.log(unzipcheck);
          [...unzipcheck].forEach(element => {
            if (element.checked){
              console.log(element.id);
              document.getElementById('mail_' + element.id).remove()
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: false
                })
              })
              load_mailbox('inbox');
             }
          })
        }
        //
  }

}