import * as React from "react";
import { View, StyleSheet, Text, ActivityIndicator } from "react-native";
import { Image, Rating, Icon } from "react-native-elements";
import Color from "../Cons/Color";
import { ScrollView } from "react-native-gesture-handler";

export default function CatalogueList(props) {
  const title = props.title;
  const issue = props.issue;
  const image = props.image;
  const price = parseInt(props.price);
  const rating = parseFloat(props.rating);
  const likes = parseInt(props.likes);
  const description = props.description;

  return (
    <View
      style={{
        width: "85%",
        backgroundColor: Color.subtle_primary,
        borderRadius: 20,
        overflow: "hidden",
        padding: 15,
        marginTop: 10,
        marginBottom: 5,
      }}
    >
      <View
        style={{
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
          paddingRight: 20,
          marginBottom: 10,
        }}
      >
        <ScrollView style={{ width: "80%", maxHeight: 50, marginLeft: 5 }}>
          <Text style={{ fontSize: 20, fontWeight: "bold" }}>{title}</Text>
        </ScrollView>
        <Text style={{ fontSize: 16, fontStyle: "italic" }}>{issue}</Text>
      </View>
      <View
        style={{
          flexDirection: "row",
          justifyContent: "space-evenly",
          alignItems: "center",
          paddingLeft: 10,
          marginBottom: 10,
        }}
      >
        <View style={{ marginRight: 10, borderRadius: 20, overflow: "hidden" }}>
          <Image
            source={image}
            style={{ width: 160, height: 160 }}
            PlaceholderContent={<ActivityIndicator />}
          />
        </View>
        <View
          style={{
            padding: 10,
            backgroundColor: "white",
            borderRadius: 20,
          }}
        >
          <View style={styles.generic_info}>
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>
              Price: ${price}
            </Text>
          </View>
          <View style={styles.generic_info}>
            <Text style={styles.generic_info_text}>Rating:</Text>
            <Rating
              type="custom"
              ratingBackgroundColor={Color.subtle_light_grey}
              readonly={true}
              startingValue={rating}
              imageSize={24}
            />
          </View>
          <View style={styles.generic_info}>
            <Text style={styles.generic_info_text}>Likes:</Text>
            <View
              style={{
                flexDirection: "row",
                justifyContent: "flex-start",
                paddingLeft: 5,
                alignItems: "center",
              }}
            >
              <Icon name="thumb-up" size={25} />
              <Text style={{ marginLeft: 5 }}>{likes}</Text>
            </View>
          </View>
        </View>
      </View>
      {!props.noDescription && (
        <View
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <ScrollView
            style={{
              width: "90%",
              height: 70,
              backgroundColor: "white",
              paddingLeft: 10,
              paddingRight: 10,
            }}
          >
            <Text>{description}</Text>
          </ScrollView>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  generic_info: {
    marginBottom: 2,
  },
  generic_info_text: {
    fontSize: 14,
  },
});
