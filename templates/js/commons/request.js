window.request = ({ url, method = "get", body = {} }) =>
  new Promise((resolve) => {
    if (!url) return console.error("No url privided") & resolve(null);
    body = ["get", "head"].includes(method.toLowerCase())
      ? undefined
      : JSON.stringify(body);
    const headers = { "Content-Type": "application/json" };

    fetch(new Request(url, { method, body, headers }))
      .then(async (Res) => {
        const Res2 = Res.clone();
        const json = await new Promise((resolveJson) =>
          Res.json()
            .then(resolveJson)
            .catch(() => resolveJson(null))
        );
        resolve({
          body: json || (await Res2.text()),
          status: Res.status,
        });
      })
      .catch((error) => {
        console.error(error);
        resolve(null);
      });
  });
