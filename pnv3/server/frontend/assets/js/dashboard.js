const HOSTNAME = document.querySelector(`meta[name = "hostname"]`).getAttribute("value");
const DEFAULT_VALUE = "Select a file to start editing.";

// Start loading in files
new class {
    constructor() {
        this.request_files();

        // State
        this.current_file = null;
        this.unsaved_changes = false;

        // Initialize buttons
        document.querySelector("#logout").addEventListener("click", () => {
            document.cookie = "authorization=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            window.location.href = "/auth";
        });
        document.querySelector("#create-file").addEventListener("click", async () => {
            const response = await post("create", { filename: prompt("Enter filename:") });
            if (response.code !== 200) return alert(response.data.message);
            await this.request_files();
        });
        document.querySelector("#save-btn").addEventListener("click", () => this.save());
        document.querySelector("#trash-btn").addEventListener("click", () => this.trash());

        // Setup code editing
        this.editor = CodeMirror.fromTextArea(document.querySelector("textarea"), { lineNumbers: true });
        this.editor.on("change", () => { this.unsaved_changes = true; });
    }

    async save() {
        if (!this.current_file) return;
        const response = await post("write", { filename: this.current_file, content: this.editor.getValue() });
        if (response.code !== 200) return alert("Failed to save file!");
        this.unsaved_changes = false;
    }

    async trash() {
        if (!this.current_file) return;
        const response = await post("delete", { filename: this.current_file });
        if (response.code !== 200) return alert("Failed to delete file!");
        this.request_files();
        this.editor.setValue(DEFAULT_VALUE);
        this.unsaved_changes = false;
    }

    async get_file(file) {
        const response = await fetch(`/v1/${HOSTNAME}/page/${file}`);
        if (response.headers.get("content-type") === "application/json") return console.error(await response.json());
        return await response.text();
    }

    async request_files() {
        const response = await (await fetch(`/v1/${HOSTNAME}/pages`)).json();
        if (response.code !== 200) return console.error(response);

        // Remove existing buttons
        for (const button of document.querySelectorAll(".page-button")) button.remove();
        
        // Add in new ones
        for (const page of response.data.pages) {
            const page_element = document.createElement("button");
            page_element.classList.add("page-button");
            page_element.innerText = `${page}.html`;
            document.querySelector("aside").insertBefore(page_element, document.querySelector(".gap"));

            // Handle changing content
            page_element.addEventListener("click", async () => {
                if (this.unsaved_changes && !confirm("You have unsaved changes, confirm loading new page?")) return;
                this.editor.setValue(await this.get_file(page));
                this.current_file = page_element.innerText;
                this.unsaved_changes = false;
            });
        }
    }
};
