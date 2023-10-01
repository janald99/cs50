document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  
  // Add event listener to compose form submission
  document.querySelector('#compose-form').addEventListener('submit', send_email);
});


function send_email() {
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
    console.log(result.message);

    // Once the email has been sent, load the "Sent" mailbox
    load_mailbox('sent');
  })
  .catch(error => {
    console.error('Error:', error);
  });

  // Clear out composition fields 
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
};

function compose_email() {
 
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
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
      emailElement.addEventListener('click', () => view_email(email.id, mailbox));

      // Append the email box to the emails-view
      emailDiv.append(emailElement);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


function view_email(emailId, mailbox) {
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

    // Check if the mailbox is NOT the "Sent" mailbox
    if (mailbox !== 'sent') {
      console.log(mailbox);
      // Add archive button
      const archiveButton = document.createElement('button');
      archiveButton.textContent = email.archived ? 'Unarchive' : 'Archive';
      archiveButton.classList.add('btn', 'btn-sm', 'btn-outline-primary');
      archiveButton.addEventListener('click', () => toggle_archive(emailId, email.archived));

      // Add reply button
      const replyButton = document.createElement('button');
      replyButton.textContent = 'Reply';
      replyButton.classList.add('btn', 'btn-sm', 'btn-outline-primary');
      replyButton.addEventListener('click', () => reply_to_email(email));

      // Append the archiveButton to the emailView
      emailView.append(archiveButton);
      // Append the replyButton to the emailView
      emailView.append(replyButton);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}



function toggle_archive(emailId, isArchived) {
  // Make a PUT request to toggle the email's archived status
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !isArchived,
    }),
  })
    .then(response => {
      if (response.status === 204) {
        console.log('Email archived/unarchived successfully.');
        // Once the email has been archived or unarchived, reload the mailbox
        load_mailbox('inbox');
      } else {
        console.error('Failed to archive/unarchive email. Status code:', response.status);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function formatTimestamp(timestamp) {
  // Create a Date object from the timestamp string
  const date = new Date(timestamp);

  // Get individual date components
  const year = date.getFullYear();
  const month = date.toLocaleString('default', { month: 'short' });
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, '0'); // Add leading zeros
  const ampm = hours >= 12 ? 'PM' : 'AM';

  // Format the date and time as required
  const formattedDate = `${month} ${day} ${year}, ${hours}:${minutes} ${ampm}`;

  return formattedDate;
}

function reply_to_email(email) {
  // Show the compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Pre-fill the composition form
  const recipientsField = document.querySelector('#compose-recipients');
  const subjectField = document.querySelector('#compose-subject');
  const bodyField = document.querySelector('#compose-body');

  // Pre-fill recipient field with the sender of the original email
  recipientsField.value = email.sender;

  // Pre-fill subject line
  let subject = email.subject;
  if (!subject.startsWith('Re: ')) {
    subject = `Re: ${subject}`;
  }
  subjectField.value = subject;

  // Pre-fill body of the email
  const originalTimestamp = formatTimestamp(email.timestamp);
  const originalSender = email.sender;
  const originalBody = email.body;
  const replyBody = `On ${originalTimestamp} ${originalSender} wrote:\n${originalBody}`;
  bodyField.value = replyBody;
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