import * as React from "react";
import { View, ActivityIndicator } from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as Permissions from "expo-permissions";
import { Button, Image } from "react-native-elements";

export default class InputImage extends React.Component {
  state = {
    image: null,
  };

  render() {
    let { image } = this.state;

    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <Button
          title="Pick an image from camera roll"
          onPress={() => this._getImage("roll")}
        />
        <Button
          title="Use Camera to take picture"
          onPress={() => this._getImage("cam")}
        />
        {image && (
          <Image
            source={{ uri: image }}
            style={{ width: 200, height: 300 }}
            PlaceholderContent={<ActivityIndicator />}
          />
        )}
      </View>
    );
  }

  componentDidMount() {
    this.getPermissionAsync();
  }

  getPermissionAsync = async () => {
    const per1 = await Permissions.askAsync(Permissions.CAMERA_ROLL);
    if (per1["status"] !== "granted") {
      alert("Sorry, we need camera roll permissions to make this work!");
    }
    const per2 = await Permissions.askAsync(Permissions.CAMERA);
    if (per2["status"] !== "granted") {
      alert("Sorry, we need camera permissions!");
    }
  };

  _getImage = async (mode) => {
    try {
      if (mode == "roll") {
        launch = ImagePicker.launchImageLibraryAsync;
      } else {
        launch = ImagePicker.launchCameraAsync;
      }
      let result = await launch({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [2, 3],
        quality: 1,
      });
      if (!result.cancelled) {
        this.setState({ image: result.uri });
      }

      console.log(result);
    } catch (E) {
      console.log(E);
    }
  };
}
