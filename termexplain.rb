class Termexplain < Formula
  include Language::Python::Virtualenv

  desc "AI-powered CLI error explainer using Gemini"
  homepage "https://github.com/smundhra-git/termExplain"
  url "https://github.com/smundhra-git/termExplain/archive/refs/tags/v1.0.1.tar.gz"
  sha256 "" #sha256 is being updated in the other github repo only
  license "MIT"
  head "https://github.com/smundhra-git/termExplain.git", branch: "main"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
    bin.install "explain.sh" => "explain"
    chmod 0755, bin/"explain"
  end

  resource "google-generativeai" do
    url "https://files.pythonhosted.org/packages/e9/87/105111999772ec9730e3d4d910c723ea9763ece2ec441533a5cea1e87e3c/click-8.2.2.tar.gz"
    sha256 "068616e6ef9705a07b6db727cb9c248f4eb9dae437a30239f56fa94b18b852ef"
  end
  
  resource "click" do
    url "https://files.pythonhosted.org/packages/fe/75/af448d8e52bf1d8fa6a9d089ca6c07ff4453d86c65c145d0a300bb073b9b/rich-14.1.0.tar.gz"
    sha256 "e497a48b844b0320d45007cdebfeaeed8db2a4f4bcf49f15e455cfc4af11eaa8"
  end
  
  resource "rich" do
    url "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz"
    sha256 "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44"
  end
  
  resource "colorama" do
    url "https://files.pythonhosted.org/packages/f6/b0/4bc07ccd3572a2f9df7e6782f52b0c6c90dcbb803ac4a167702d7d0dfe1e/python_dotenv-1.1.1.tar.gz"
    sha256 "a8a6399716257f45be6a007360200409fce5cda2661e3dec71d23dc15f6189ab"
  end
  
  resource "python-dotenv" do
    url "https://files.pythonhosted.org/packages/e1/0a/929373653770d8a0d7ea76c37de6e41f11eb07559b103b1c02cafb3f7cf8/requests-2.32.4.tar.gz"
    sha256 "27d0316682c8a29834d3264820024b62a36942083d52caf2f14c0591336d3422"
  end
  
  resource "requests" do
    url "https://files.pythonhosted.org/packages/e1/0a/929373653770d8a0d7ea76c37de6e41f11eb07559b103b1c02cafb3f7cf8/requests-2.32.4.tar.gz"
    sha256 "27d0316682c8a29834d3264820024b62a36942083d52caf2f14c0591336d3422"
  end
  
  def install
    venv = virtualenv_create(libexec, "python3.11")
    venv.pip_install resources
    venv.pip_install_and_link buildpath
  end

  test do
    assert_match "error", shell_output("#{bin}/explain 'ModuleNotFoundError'", 1)
  end

  test do
    system "#{bin}/explain", "echo 'Test error'"
  end

  def caveats
    <<~EOS
      termExplain requires a Gemini API key to function.

      Set your API key:
        export GEMINI_API_KEY="your-api-key-here"

      Or add to your shell profile (~/.zshrc or ~/.bashrc):
        echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc

      Get your API key from: https://aistudio.google.com/

      Usage:
        explain "your error message here"
    EOS
  end
end
