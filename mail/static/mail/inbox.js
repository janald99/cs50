document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  
});

function compose_email() {
 
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Add event listener to compose form submission
  document.querySelector('#compose-form').addEventListener('submit', function (event) {
    // Prevent default form submission behavior
    event.preventDefault();

    // Collect form data
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // Send a post request to /emails to send email
    console.log("fetching /emails");
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      }),
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result.message);

      // Once the email has been sent, you can load the "Sent" mailbox
      load_mailbox('sent');
    })
    .catch(error => {
      // Handle errors, e.g., display an error message
      console.log("aweaefwfwf");
      console.error('Error:', error);
    });

    // Clear out composition fields (optional, you can leave this here)
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails from specified mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    const emailDiv = document.querySelector('#emails-view');

    // Clear the existing content
    emailDiv.innerHTML = '';

    // Iterate through each email and render it in its own box
    emails.forEach(email => {
      const emailElement = document.createElement('div');
      emailElement.classList.add('email');

      // Check if the email is read or unread
      if (email.read) {
        emailElement.classList.add('email-read'); // Add the 'email-read' class for read emails
      } else {
        emailElement.classList.add('email-unread'); // Add the 'email-unread' class for unread emails
      }

      // Construct the email box content
      emailElement.innerHTML = `
      <strong>From:</strong> ${email.sender}<br>
      <strong>Subject:</strong> ${email.subject}<br>
      <strong>Timestamp:</strong> ${email.timestamp}<br>
    `;

      // Add a click event listener to view the email when clicked
      emailElement.addEventListener('click', () => view_email(email.id));


      // Append the email box to the emails-view
      emailDiv.appendChild(emailElement);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


function view_email(emailId) {
  // GET request to fetch email details
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    // Update the email-view element to display the email details
    const emailView = document.querySelector('#email-view');
    emailView.innerHTML = `
      <h2>From: ${email.sender}</h2>
      <h3>To: ${email.recipients.join(', ')}</h3>
      <p>Subject: ${email.subject}</p>
      <p>Timestamp: ${email.timestamp}</p>
      <hr>
      <p>${email.body}</p>
    `;

    // Show the email-view and hide the emails-view
    document.querySelector('#emails-view').style.display = 'none';
    emailView.style.display = 'block';

      // Mark email as read by sending put request
      mark_email_as_read(emailId);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function mark_email_as_read(emailId) {
  // Make a PUT request to mark the email as read
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true,
    }),
  }).catch(error => {
    console.error('Error:', error);
  });
}