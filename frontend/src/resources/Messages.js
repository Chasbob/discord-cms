import * as React from "react";
import {
  List,
  Datagrid,
  Edit,
  Create,
  SimpleForm,
  DateField,
  TextField,
  EditButton,
  TextInput,
  DateInput,
  useAuthenticated,
} from "react-admin";
// import BookIcon from "@material-ui/core/svg-icons/action/book";
// export const MessageIcon = BookIcon;

export const MessageList = (props) => {
  useAuthenticated(); // redirects to login if not authenticated
  return (
    <List {...props}>
      <Datagrid>
        <TextField source="id" />
        <TextField source="name" />
        <TextField source="channel" />
        <TextField source="content" />
        <TextField source="user" />
        <EditButton basePath="/messages" />
      </Datagrid>
    </List>
  );
};

const MessageTitle = ({ record }) => {
  return <span>Message {record ? `"${record.title}"` : ""}</span>;
};

export const MessageEdit = (props) => {
  useAuthenticated();
  return (
    <Edit title={<MessageTitle />} {...props}>
      <SimpleForm>
        <TextInput source="name" />
        <TextInput multiline source="content" />
        <TextInput disabled source="channel" />
      </SimpleForm>
    </Edit>
  );
};

export const MessageCreate = (props) => (
  <Create title="Create a Message" {...props}>
    <SimpleForm>
      <TextInput source="title" />
      <TextInput source="teaser" options={{ multiLine: true }} />
      <TextInput multiline source="body" />
      <TextInput label="Publication date" source="published_at" />
      <TextInput source="average_note" />
    </SimpleForm>
  </Create>
);
