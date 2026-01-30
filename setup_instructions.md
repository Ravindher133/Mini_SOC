# React Native Development Environment Setup Instructions

To run your React Native application on Android, you need to set up your development environment correctly. Please follow these steps:

## 1. Install the Java Development Kit (JDK)

React Native requires a specific version of the Java Development Kit (JDK). We recommend using **JDK 11**.

1.  **Download:** You can download an installer for JDK 11 from [Oracle's website](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html) or use an open-source alternative like [Adoptium's Temurin](https://adoptium.net/temurin/releases/?version=11). You will need to create an Oracle account to download from their website.
2.  **Install:** Run the installer and follow the on-screen instructions.

## 2. Set the `JAVA_HOME` Environment Variable

After installing the JDK, you need to set the `JAVA_HOME` environment variable.

1.  **Find the JDK installation path:** The default installation path is usually `C:\Program Files\Java\jdk-11.x.x` or `C:\Program Files\AdoptOpenJDK\jdk-11.x.x.x-hotspot\`.
2.  **Set the environment variable:**
    *   Open the **Control Panel** and go to **System and Security** > **System**.
    *   Click on **Advanced system settings** on the left.
    *   Click the **Environment Variables...** button.
    *   Under **System variables**, click **New...**.
    *   For **Variable name**, enter `JAVA_HOME`.
    *   For **Variable value**, enter the path to your JDK installation (e.g., `C:\Program Files\Java\jdk-11.0.12`).
    *   Click **OK**.

## 3. Install Android Studio

Android Studio is the official IDE for Android development, and it includes the Android SDK and other necessary tools.

1.  **Download:** Download Android Studio from the [official website](https://developer.android.com/studio).
2.  **Install:** Run the installer and follow the on-screen instructions. Make sure to select the following components during installation:
    *   Android SDK
    *   Android SDK Platform
    *   Android Virtual Device

## 4. Configure the `ANDROID_HOME` Environment Variable

1.  **Set the environment variable:**
    *   Open the **Control Panel** > **System and Security** > **System** > **Advanced system settings** > **Environment Variables...**.
    *   Under **System variables**, click **New...**.
    *   For **Variable name**, enter `ANDROID_HOME`.
    *   For **Variable value**, enter the path to your Android SDK. The default location is `C:\Users\%USERNAME%\AppData\Local\Android\Sdk`.
    *   Click **OK**.

## 5. Add Android Platform-Tools to the PATH

1.  **Edit the `Path` variable:**
    *   In the **Environment Variables** window, find the `Path` variable under **System variables** and click **Edit...**.
    *   Click **New** and add the following path: `%ANDROID_HOME%\platform-tools`.
    *   Click **OK** to close all the windows.

## 6. Restart your computer

After making these changes, it's a good idea to restart your computer to ensure all the changes take effect.

After you have completed these steps, you should be able to run `npx react-native run-android` successfully.
