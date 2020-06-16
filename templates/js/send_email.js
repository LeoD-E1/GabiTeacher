// {% if not paths %}{% set paths = [] %}{% endif %}
// {% set path = 'js/commons/request.js' %}
// {% if not path in paths %}{{paths.append(path)}}{{'\n'}}{% include path %}{% endif %}
(() => {
  let sent = false;
  const email = document.getElementById("email");
  const name = document.getElementById("name");
  const subject = document.getElementById("subject");
  const message = document.getElementById("message");

  window.send_email = async () => {
    if (sent) return;
    sent = true;
    console.log("send_email");
    const body = {
      to: "{{ contact_emails }}".split(","),
      subject: `Contacto: ${subject.value}`,
      data: {
        name: name.value,
        email: email.value,
        message: message.value.replace(/\n/g, "<br>"),
      },
    };
    const result = await window.request({
      url: "/api/email/contact",
      method: "post",
      body: JSON.stringify(body),
    });
    if (!result || result.status !== 200) {
      sent = false;
      return alert("Algo salió mal, intenta mas tarde");
    }
    alert("Mail enviado OK");
  };
})();
