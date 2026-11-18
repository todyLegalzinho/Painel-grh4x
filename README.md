# GRH4X Red Panel — cloud APK build

This is a standalone Kivy Android configuration/training simulator with a black/red panel UI.
It is not Grh4x, is not affiliated with Garena, and does not interact with Free Fire.
The Aimbot/ESP-labelled switches are visual-only demonstrations inside this app.
No tool can guarantee that a cheat avoids bans; this project does not implement game cheats.

## Build the APK using only your phone

You need a GitHub account. You do not need a computer or Linux installation.

1. Download and extract this ZIP on your phone.
2. In your phone browser, open https://github.com/new and create a **Public** repository named `grh4x-red-panel`.
   (A private repository also works if GitHub Actions is available on your account.)
3. On the new repository page, choose **Add file → Upload files**.
4. Upload `main.py`, `buildozer.spec`, and the `.github` folder (including `workflows/android.yml`).
   If the mobile upload page does not preserve the nested `.github/workflows` folders, use GitHub's web editor to create the file at:
   `.github/workflows/android.yml`
   and paste the workflow from this ZIP.
5. Commit the files to the `main` branch.
6. Open the repository's **Actions** tab. Select **Build Android APK**, then **Run workflow** if it has not started automatically.
7. Wait for the run to finish with a green checkmark.
8. Open the completed run. Under **Artifacts**, download `GRH4X-Red-Panel-APK`.
9. Extract the artifact ZIP on your phone. It contains the `.apk`.
10. Tap the APK to install. Android may ask you to allow installs from your browser or file manager.

## Notes
- The first build can take several minutes because Android SDK/NDK components are downloaded.
- GitHub Actions minutes and account limits may apply.
- This workflow creates a debug APK for personal testing, not a Play Store release.
- If the build fails, open the failed Actions run and share the error log so it can be fixed.
