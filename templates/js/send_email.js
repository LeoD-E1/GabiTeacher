// {% if not paths %}{% set paths = [] %}{% endif %}
// {% set path = 'js/commons/request.js' %}
// {% if not path in paths %}{{paths.append(path)}}{{'\n'}}{% include path %}{% endif %}
window.send_email = () => {
  console.log("send_email");
};
